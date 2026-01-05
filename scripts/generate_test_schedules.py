#!/usr/bin/env python3
"""
生成测试排班数据 - 基于已有的义工和活动数据
"""
import sys
import os
import random
import time
from datetime import datetime, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.schedule import ScheduleModel
from models.volunteer import VolunteerModel
from models.event import EventModel

# 担任角色选项
ROLES = [
    '接待员',
    '清洁员',
    '摄影员',
    '协助人',
    '负责人',
    '其他',
]

# 排班状态选项
STATUSES = [
    '已排班',
    '已确认',
    '已签到',
    '已签退',
    '缺席',
]

# 工作表现选项
PERFORMANCES = [
    '优秀',
    '良好',
    '一般',
    '需改进',
]

# 备注内容
REMARKS = [
    '积极配合',
    '表现良好',
    '需要后续培训',
    '有缺席',
    '表现优秀',
    '',
]

def get_field_value(data, field_key, default=''):
    """安全地获取字段值，支持两种格式"""
    value = data.get(field_key, default)
    
    # 如果是字典格式 {'value': ...}
    if isinstance(value, dict):
        return value.get('value', default)
    # 如果是直接的字符串或其他类型
    return value if value else default

def extract_time_only(datetime_str):
    """从日期时间字符串中提取时间部分（HH:MM）"""
    if not datetime_str:
        return ''
    # 如果是 "2026-03-16 08:30:00" 格式，提取 "08:30"
    if ' ' in datetime_str:
        time_part = datetime_str.split(' ')[1]
        return time_part.split(':')[0] + ':' + time_part.split(':')[1]  # HH:MM
    return ''

def generate_schedule(volunteer_data, event_data):
    """生成一条排班记录"""
    
    # 从义工档案表中获取数据
    volunteer_name = get_field_value(volunteer_data, VolunteerModel.FIELD_NAME, '')
    volunteer_phone = get_field_value(volunteer_data, VolunteerModel.FIELD_PHONE, '')
    volunteer_gender = get_field_value(volunteer_data, VolunteerModel.FIELD_GENDER, '')
    
    # 检查必需字段
    if not volunteer_name or not volunteer_phone:
        return None
    
    event_name = get_field_value(event_data, EventModel.FIELD_EVENT_NAME, '未知活动')
    event_date = get_field_value(event_data, EventModel.FIELD_EVENT_DATE, '')
    start_time = get_field_value(event_data, EventModel.FIELD_START_TIME, '')
    end_time = get_field_value(event_data, EventModel.FIELD_END_TIME, '')
    location = get_field_value(event_data, EventModel.FIELD_LOCATION, '')
    
    # 组合活动时间（HH:MM-HH:MM 格式）
    start_time_only = extract_time_only(start_time)
    end_time_only = extract_time_only(end_time)
    if start_time_only and end_time_only:
        event_time = f"{start_time_only}-{end_time_only}"
    else:
        event_time = "09:00-17:00"
    
    # 根据状态生成相应的时间信息
    check_in_time = None
    check_out_time = None
    actual_hours = None
    
    # 70% 的概率生成签到时间（包括所有状态，让数据更丰富）
    if random.random() < 0.7:
        try:
            event_date_obj = datetime.strptime(event_date, '%Y-%m-%d')
            check_in_hour = random.randint(8, 10)
            check_in_minute = random.choice([0, 15, 30, 45])
            check_in_second = random.randint(0, 59)
            check_in_time = event_date_obj.strftime('%Y-%m-%d') + f" {check_in_hour:02d}:{check_in_minute:02d}:{check_in_second:02d}"
        except:
            check_in_time = None
    
    # 在有签到时间的基础上，50% 概率生成签退时间（已签退或部分签到）
    if check_in_time and random.random() < 0.5:
        try:
            check_in_dt = datetime.strptime(check_in_time, '%Y-%m-%d %H:%M:%S')
            hours_worked = random.randint(2, 8)
            check_out_second = random.randint(0, 59)
            check_out_dt = check_in_dt + timedelta(hours=hours_worked, seconds=check_out_second)
            check_out_time = check_out_dt.strftime('%Y-%m-%d %H:%M:%S')
            actual_hours = hours_worked
            # 如果有签退，把状态改为已签退
            status = '已签退'
        except:
            check_out_time = None
            status = random.choice(STATUSES)
    else:
        status = random.choice(STATUSES)
    
    data = {
        ScheduleModel.FIELD_NAME: volunteer_name,
        ScheduleModel.FIELD_PHONE: volunteer_phone,
        ScheduleModel.FIELD_GENDER: volunteer_gender,  # 从义工档案表获取
        ScheduleModel.FIELD_EVENT_NAME: event_name,
        ScheduleModel.FIELD_EVENT_DATE: event_date,
        ScheduleModel.FIELD_EVENT_TIME: event_time,
        ScheduleModel.FIELD_LOCATION: location,
        ScheduleModel.FIELD_ROLE: random.choice(ROLES),
        ScheduleModel.FIELD_STATUS: status,
        ScheduleModel.FIELD_WORK_PERFORMANCE: random.choice(PERFORMANCES) if status in ['已签退', '已签到'] else '',
        ScheduleModel.FIELD_REMARKS: random.choice(REMARKS),
    }
    
    # 只在状态为已签到或已签退时才添加时间信息
    if check_in_time:
        data[ScheduleModel.FIELD_CHECK_IN_TIME] = check_in_time
    if check_out_time:
        data[ScheduleModel.FIELD_CHECK_OUT_TIME] = check_out_time
    if actual_hours:
        data[ScheduleModel.FIELD_ACTUAL_HOURS] = actual_hours
    
    return data
    
    return data

def batch_create_schedules(schedules_per_event=5):
    """批量创建排班记录"""
    
    print("🚀 开始生成排班签到数据")
    print("=" * 70)
    
    # 获取所有义工
    try:
        volunteers_df = VolunteerModel.list_all()
        if volunteers_df.empty:
            print("❌ 没有找到任何义工数据！请先生成义工数据。")
            return
        volunteers = volunteers_df.to_dict('records')
        print(f"✅ 找到 {len(volunteers)} 个义工")
    except Exception as e:
        print(f"❌ 获取义工数据失败: {e}")
        return
    
    # 获取所有活动
    try:
        events_df = EventModel.list_all()
        if events_df.empty:
            print("❌ 没有找到任何活动数据！请先生成活动数据。")
            return
        events = events_df.to_dict('records')
        print(f"✅ 找到 {len(events)} 个活动")
    except Exception as e:
        print(f"❌ 获取活动数据失败: {e}")
        return
    
    print("\n" + "=" * 70)
    print(f"📊 准备为每个活动分配 {schedules_per_event} 个义工\n")
    
    success_count = 0
    fail_count = 0
    
    # 为每个活动分配义工
    for event_idx, event in enumerate(events):
        # 每个活动分配 schedules_per_event 个义工
        for _ in range(schedules_per_event):
            try:
                # 随机选择一个义工
                volunteer = random.choice(volunteers)
                
                # 生成排班数据（传入完整的义工对象）
                schedule_data = generate_schedule(volunteer, event)
                
                if not schedule_data:
                    continue
                
                # 创建排班记录
                schedule_id = ScheduleModel.create(**schedule_data)
                
                if schedule_id:
                    success_count += 1
                else:
                    fail_count += 1
                
                # 限流
                time.sleep(0.1)
                
            except Exception as e:
                fail_count += 1
                if fail_count % 10 == 0:
                    print(f"❌ 第 {fail_count} 条创建失败: {str(e)[:60]}")
        
        # 每处理完 5 个活动就打印一次进度
        if (event_idx + 1) % 5 == 0:
            print(f"✅ 已处理 {event_idx + 1}/{len(events)} 个活动 (成功: {success_count}, 失败: {fail_count})")
    
    print("\n" + "=" * 70)
    print(f"✅ 排班数据生成完成！")
    print(f"   总数: {success_count + fail_count}")
    print(f"   成功: {success_count}")
    print(f"   失败: {fail_count}")
    if (success_count + fail_count) > 0:
        print(f"   成功率: {(success_count/(success_count + fail_count))*100:.1f}%")
    
    # 验证数据
    try:
        total = ScheduleModel.get_schedule_count()
        print(f"\n📊 数据库中排班总数: {total}")
        
        statuses = {}
        for status in ['已排班', '已确认', '已签到', '已签退', '缺席']:
            count = len(ScheduleModel.list_by_status(status))
            if count > 0:
                statuses[status] = count
        
        if statuses:
            print(f"   按状态分布:")
            for status, count in statuses.items():
                print(f"     - {status}: {count}")
            
    except Exception as e:
        print(f"❌ 验证失败: {e}")

if __name__ == "__main__":
    batch_create_schedules(schedules_per_event=5)