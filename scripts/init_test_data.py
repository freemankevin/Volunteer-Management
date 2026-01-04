#!/usr/bin/env python3
"""
初始化测试数据
模拟真实场景，批量创建义工、活动、排班数据
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.volunteer import VolunteerModel
from models.event import EventModel
from models.schedule import ScheduleModel
from datetime import datetime, timedelta

# 测试义工数据
VOLUNTEERS = [
    {
        "name": "张三",
        "phone": "13800138000",
        "age": 35,
        "gender": "男",
        "skills": "医疗、急救",
        "status": "活跃"
    },
    {
        "name": "李四",
        "phone": "13800138001",
        "age": 28,
        "gender": "女",
        "skills": "摄影、文书",
        "status": "活跃"
    },
    {
        "name": "王五",
        "phone": "13800138002",
        "age": 42,
        "gender": "男",
        "skills": "组织协调",
        "status": "活跃"
    },
    {
        "name": "赵六",
        "phone": "13800138003",
        "age": 31,
        "gender": "女",
        "skills": "翻译、接待",
        "status": "活跃"
    },
    {
        "name": "孙七",
        "phone": "13800138004",
        "age": 25,
        "gender": "男",
        "skills": "技术支持",
        "status": "暂停"
    }
]

# 测试活动数据
EVENTS = [
    {
        "event_name": "春节祈福法会",
        "event_type": "法会活动",
        "event_date": "2024-02-10",
        "start_time": "09:00",
        "end_time": "17:00",
        "location": "大雄宝殿",
        "status": "计划中"
    },
    {
        "event_name": "清明祭祖活动",
        "event_type": "祭祀活动",
        "event_date": "2024-04-05",
        "start_time": "08:00",
        "end_time": "12:00",
        "location": "墓地",
        "status": "计划中"
    },
    {
        "event_name": "盂兰盆法会",
        "event_type": "法会活动",
        "event_date": "2024-08-15",
        "start_time": "09:00",
        "end_time": "18:00",
        "location": "大雄宝殿",
        "status": "计划中"
    },
    {
        "event_name": "寺院卫生清洁",
        "event_type": "清洁活动",
        "event_date": "2024-03-15",
        "start_time": "08:00",
        "end_time": "12:00",
        "location": "寺院全地",
        "status": "报名中"
    },
    {
        "event_name": "佛学知识讲座",
        "event_type": "教育活动",
        "event_date": "2024-02-20",
        "start_time": "14:00",
        "end_time": "16:00",
        "location": "讲堂",
        "status": "进行中"
    }
]

def init_volunteers():
    """初始化义工数据"""
    print("\n=== 初始化义工数据 ===")
    volunteer_ids = []
    
    for vol in VOLUNTEERS:
        try:
            vol_id = VolunteerModel.create(**vol)
            if vol_id:
                volunteer_ids.append(vol_id)
                print(f"✅ 创建义工: {vol['name']} (ID: {vol_id[:8]}...)")
            else:
                print(f"⚠️  创建义工 {vol['name']} 返回空ID")
                volunteer_ids.append(None)
        except Exception as e:
            print(f"❌ 创建义工 {vol['name']} 失败: {e}")
            volunteer_ids.append(None)
    
    print(f"\n✅ 义工初始化完成，共创建 {sum(1 for x in volunteer_ids if x)} 条数据")
    return volunteer_ids

def init_events():
    """初始化活动数据"""
    print("\n=== 初始化活动数据 ===")
    event_ids = []
    
    for event in EVENTS:
        try:
            event_id = EventModel.create(**event)
            if event_id:
                event_ids.append(event_id)
                print(f"✅ 创建活动: {event['event_name']} (ID: {event_id[:8]}...)")
            else:
                print(f"⚠️  创建活动 {event['event_name']} 返回空ID")
                event_ids.append(None)
        except Exception as e:
            print(f"❌ 创建活动 {event['event_name']} 失败: {e}")
            event_ids.append(None)
    
    print(f"\n✅ 活动初始化完成，共创建 {sum(1 for x in event_ids if x)} 条数据")
    return event_ids

def init_schedules(volunteer_ids, event_ids):
    """初始化排班数据"""
    print("\n=== 初始化排班数据 ===")
    
    # 过滤掉为空的ID
    valid_vols = [(i, vol_id) for i, vol_id in enumerate(volunteer_ids) if vol_id]
    valid_events = [(i, event_id) for i, event_id in enumerate(event_ids) if event_id]
    
    if not valid_vols or not valid_events:
        print("❌ 没有有效的义工或活动数据，无法创建排班")
        return
    
    schedule_count = 0
    roles = ["接待员", "清洁员", "摄影员", "协助人", "负责人"]
    
    # 为每个活动分配义工
    for event_idx, event_id in valid_events:
        event = EVENTS[event_idx]
        
        # 每个活动分配3-5个义工
        num_volunteers = min(3 + event_idx % 2, len(valid_vols))
        
        for j in range(num_volunteers):
            vol_idx, vol_id = valid_vols[j]
            vol = VOLUNTEERS[vol_idx]
            
            schedule_data = {
                "volunteer_name": vol['name'],
                "volunteer_phone": vol['phone'],
                "event_name": event['event_name'],
                "event_date": event['event_date'],
                "role": roles[j % len(roles)],
                "status": "已排班"
            }
            
            try:
                schedule_id = ScheduleModel.create(**schedule_data)
                if schedule_id:
                    schedule_count += 1
                    print(f"✅ 排班: {vol['name']} → {event['event_name']} ({schedule_data['role']})")
            except Exception as e:
                print(f"❌ 排班失败: {vol['name']} → {event['event_name']}: {e}")
    
    print(f"\n✅ 排班初始化完成，共创建 {schedule_count} 条排班记录")

def verify_data():
    """验证创建的数据"""
    print("\n=== 数据统计 ===")
    
    try:
        vol_count = VolunteerModel.get_volunteer_count()
        print(f"✅ 义工总数: {vol_count}")
        
        event_count = EventModel.get_event_count()
        print(f"✅ 活动总数: {event_count}")
        
        schedule_count = ScheduleModel.get_schedule_count()
        print(f"✅ 排班总数: {schedule_count}")
        
        # 按状态统计
        active = len(VolunteerModel.list_by_status("活跃"))
        print(f"   - 活跃义工: {active}")
        
        events_planning = len(EventModel.list_by_status("计划中"))
        print(f"   - 计划中活动: {events_planning}")
        
    except Exception as e:
        print(f"❌ 统计失败: {e}")

if __name__ == "__main__":
    print("🚀 开始初始化测试数据")
    print("=" * 60)
    
    # 创建数据
    volunteer_ids = init_volunteers()
    event_ids = init_events()
    init_schedules(volunteer_ids, event_ids)
    
    # 验证数据
    verify_data()
    
    print("\n" + "=" * 60)
    print("✅ 测试数据初始化完成！")
    print("\n可以开始测试了：")
    print("  python test_api.py")