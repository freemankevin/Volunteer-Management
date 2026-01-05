#!/usr/bin/env python3
"""
生成 200 条测试义工数据 - 广州地区版本
支持复选框技能字段
"""
import sys
import os
import random
from datetime import datetime, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.volunteer import VolunteerModel

# 姓名数据
FIRST_NAMES = ['张', '李', '王', '赵', '孙', '周', '吴', '郑', '刘', '陈', '杨', '黄', '何', '萧', '曾']
LAST_NAMES = ['三', '四', '五', '六', '七', '八', '九', '十', '一', '二', '勇', '强', '健', '超', '明']

# 技能特长 - 复选框格式（列表）
SKILLS = [
    ['编程'],
    ['法务'],
    ['会计'],
    ['外语'],
    ['摄影'],
    ['书法'],
    ['唱歌'],
    ['乐器'],
    ['安保'],
    ['开车'],
    ['园艺'],
    ['其他'],
    ['编程', '外语'],
    ['摄影', '书法'],
    ['会计', '法务'],
    ['唱歌', '乐器'],
    ['编程', '会计'],
    ['外语', '摄影'],
    ['书法', '唱歌'],
    ['安保', '开车'],
]

# 广州常住区域 - 11个行政区
AREAS = [
    '天河区',
    '越秀区',
    '海珠区',
    '荔湾区',
    '黄埔区',
    '番禺区',
    '花都区',
    '从化区',
    '增城区',
    '南沙区',
    '白云区',
]

# 可服务时段 - 复选框格式
TIME_SLOTS = [
    ['上午'],           # 08:00 ~ 12:00
    ['下午'],           # 12:00 ~ 04:30
    ['晚上'],           # 19:00 ~ 21:00
    ['上午', '下午'],
    ['下午', '晚上'],
    ['上午', '晚上'],
    ['上午', '下午', '晚上'],
]

# 状态分布
STATUSES = ['活跃', '活跃', '活跃', '活跃', '活跃', '暂停', '退出']

# 是否皈依
ORDAINED = ['是', '否', '否', '否']

def generate_phone():
    """生成手机号"""
    return '1' + str(random.choice([3, 5, 6, 7, 8, 9])) + ''.join([str(random.randint(0, 9)) for _ in range(9)])

def generate_id_card():
    """生成身份证号（仅作示例）"""
    return ''.join([str(random.randint(0, 9)) for _ in range(18)])

def generate_name():
    """生成姓名"""
    first = random.choice(FIRST_NAMES)
    last = random.choice(LAST_NAMES)
    return first + last

def generate_volunteer():
    """生成一条义工数据"""
    age = random.randint(18, 70)
    gender = random.choice(['男', '女'])
    ordained = random.choice(ORDAINED)
    
    # 生成皈依日期（如果皈依）
    ordained_date = None
    dharma_name = None
    if ordained == '是':
        days_ago = random.randint(30, 3650)
        ordained_date = (datetime.now() - timedelta(days=days_ago)).strftime('%Y-%m-%d')
        dharma_names = ['观音', '地藏', '文殊', '普贤', '慧能', '法海', '玄奘', '鉴真', '觉悟', '静慧']
        dharma_name = random.choice(dharma_names) + str(random.randint(100, 999))
    
    # 加入日期
    join_days_ago = random.randint(1, 3650)
    join_date = (datetime.now() - timedelta(days=join_days_ago)).strftime('%Y-%m-%d')
    
    data = {
        VolunteerModel.FIELD_NAME: generate_name(),
        VolunteerModel.FIELD_PHONE: generate_phone(),
        VolunteerModel.FIELD_ID_CARD: generate_id_card(),
        VolunteerModel.FIELD_AGE: age,
        VolunteerModel.FIELD_GENDER: gender,
        VolunteerModel.FIELD_SKILLS: random.choice(SKILLS),  # 复选框格式：列表
        VolunteerModel.FIELD_AREA: random.choice(AREAS),
        VolunteerModel.FIELD_AVAILABLE_TIME: random.choice(TIME_SLOTS),  # 复选框格式：列表
        VolunteerModel.FIELD_IS_ORDAINED: ordained,
        VolunteerModel.FIELD_JOIN_DATE: join_date,
        VolunteerModel.FIELD_STATUS: random.choice(STATUSES),
    }
    
    # 条件字段
    if ordained_date:
        data[VolunteerModel.FIELD_ORDAINED_DATE] = ordained_date
    if dharma_name:
        data[VolunteerModel.FIELD_DHARMA_NAME] = dharma_name
    
    # 备注
    remarks_list = [
        '经验丰富，长期参与志愿活动',
        '热心公益，积极主动',
        '特殊技能，可做专项支援',
        '新加入的义工，正在适应中',
        '兼职志愿者，时间灵活',
        '老志愿者，非常投入',
        '学生志愿者，学习与服务并行',
        '退休人员，有充足时间',
        '专业人士，可提供专业指导',
        '社区志愿者，就近服务',
        '',  # 空备注
    ]
    data[VolunteerModel.FIELD_REMARKS] = random.choice(remarks_list)
    
    return data

def batch_create_volunteers(count=200):
    """批量创建义工"""
    print(f"🚀 开始生成 {count} 条测试义工数据 (广州地区)")
    print("=" * 70)
    
    success_count = 0
    fail_count = 0
    
    for i in range(1, count + 1):
        try:
            volunteer_data = generate_volunteer()
            volunteer_id = VolunteerModel.create(**volunteer_data)
            
            if volunteer_id:
                success_count += 1
                if i % 20 == 0:
                    print(f"✅ 已创建 {i}/{count} 条数据 (成功: {success_count}, 失败: {fail_count})")
            else:
                fail_count += 1
                print(f"⚠️  第 {i} 条数据返回空ID")
                
        except Exception as e:
            fail_count += 1
            if i % 50 == 0:
                print(f"❌ 第 {i} 条数据创建失败: {str(e)[:50]}")
    
    print("\n" + "=" * 70)
    print(f"✅ 数据生成完成！")
    print(f"   总数: {count}")
    print(f"   成功: {success_count}")
    print(f"   失败: {fail_count}")
    print(f"   成功率: {(success_count/count)*100:.1f}%")
    
    # 验证数据
    try:
        total = VolunteerModel.get_volunteer_count()
        print(f"\n📊 数据库中义工总数: {total}")
        
        active = len(VolunteerModel.list_by_status('活跃'))
        print(f"   - 活跃义工: {active}")
        
        # 按区统计
        print(f"\n📍 各区义工分布:")
        for area in AREAS:
            # 这里可以添加按区统计的逻辑
            pass
            
    except Exception as e:
        print(f"❌ 验证失败: {e}")

if __name__ == "__main__":
    batch_create_volunteers(200)