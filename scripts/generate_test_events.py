#!/usr/bin/env python3
"""
生成测试活动数据 - 基于实际的活动库表字段
固定时间问题：确保所有活动在白天（8-20点）
"""
import sys
import os
import random
import time
from datetime import datetime, timedelta
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.event import EventModel

# 活动名称列表
EVENT_NAMES = [
    '春节祈福法会',
    '清明祭祖活动',
    '盂兰盆法会',
    '寺院卫生清洁',
    '佛学知识讲座',
    '端午节诵经活动',
    '中秋赏月法会',
    '冬至施食活动',
    '新年钟声开示',
    '禅修静坐班',
    '经文抄写活动',
    '慈善募捐活动',
    '文化艺术展览',
    '义工培训课程',
    '社区志愿服务',
]

# 活动类型
EVENT_TYPES = [
    '法会活动',
    '祭祀活动',
    '清洁活动',
    '教育活动',
    '文化活动',
    '慈善活动',
    '培训课程',
    '社区服务',
]

# 活动地点
LOCATIONS = [
    '大雄宝殿',
    '讲堂',
    '禅堂',
    '食堂',
    '寺院广场',
    '寺院全地',
    '客堂',
    '斋堂',
    '图书馆',
    '办公室',
]

# 活动状态
STATUSES = [
    '计划中',
    '报名中',
    '进行中',
    '已完成',
    '已取消',
]

# 所需技能（复选框格式）
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
]

# 活动描述模板
DESCRIPTIONS = [
    '这是一场庄严的法会，邀请各位居士共同参与，祈福新年安康。',
    '缅怀先人，传承孝道，共同完成祭祖的庄严仪式。',
    '清洁寺院，美化环境，提升大家的志愿服务精神。',
    '深入浅出讲解佛学经典，欢迎各位前来听讲。',
    '展现文化艺术风采，丰富寺院文化生活。',
    '汇聚爱心，帮助有需要的群体。',
    '提升义工素质，学习志愿服务技能。',
    '服务社区，回馈社会。',
    '静坐修禅，体验内心的宁静。',
    '手抄经文，修养身心。',
]

def generate_event_date():
    """生成活动日期（未来的日期，未来 1-90 天）"""
    days_ahead = random.randint(1, 90)
    event_date = datetime.now() + timedelta(days=days_ahead)
    return event_date.strftime('%Y-%m-%d')

def generate_event():
    """生成一条活动数据 - 时间必须在白天 8-20 点"""
    event_date = generate_event_date()
    
    # ============= 关键修复 =============
    # 开始时间：上午 8 点到中午 12 点
    start_hour = random.randint(8, 12)
    start_minute = random.choice([0, 30])
    start_time = f"{event_date} {start_hour:02d}:{start_minute:02d}"
    
    # 结束时间：开始时间 + 2-4 小时（保证不超过 16 点）
    end_hour = start_hour + random.randint(2, 4)
    end_minute = random.choice([0, 30])
    end_time = f"{event_date} {end_hour:02d}:{end_minute:02d}"
    # ===================================
    
    # 当前报名人数不超过需要的义工人数
    required_volunteers = random.randint(5, 50)
    current_participants = random.randint(0, required_volunteers)
    
    data = {
        EventModel.FIELD_EVENT_NAME: random.choice(EVENT_NAMES),
        EventModel.FIELD_EVENT_TYPE: random.choice(EVENT_TYPES),
        EventModel.FIELD_DESCRIPTION: random.choice(DESCRIPTIONS),
        EventModel.FIELD_EVENT_DATE: event_date,
        EventModel.FIELD_START_TIME: start_time,
        EventModel.FIELD_END_TIME: end_time,
        EventModel.FIELD_LOCATION: random.choice(LOCATIONS),
        EventModel.FIELD_REQUIRED_VOLUNTEERS: required_volunteers,
        EventModel.FIELD_CURRENT_PARTICIPANTS: current_participants,
        EventModel.FIELD_STATUS: random.choice(STATUSES),
        EventModel.FIELD_REQUIRED_SKILLS: random.choice(SKILLS),
        EventModel.FIELD_REMARKS: random.choice([
            '欢迎各位义工踊跃报名',
            '需要有经验的义工',
            '新手也可以参加',
            '报名后会有培训',
            '请提前到达',
            '',
        ]),
    }
    
    return data

def batch_create_events(count=50):
    """批量创建活动"""
    print(f"🚀 开始生成 {count} 条测试活动数据")
    print("=" * 70)
    print(f"📝 时间范围：8:00 - 16:30（白天时间）\n")
    
    success_count = 0
    fail_count = 0
    
    for i in range(1, count + 1):
        try:
            event_data = generate_event()
            event_id = EventModel.create(**event_data)
            
            if event_id:
                success_count += 1
                if i % 10 == 0:
                    print(f"✅ 已创建 {i}/{count} 条数据 (成功: {success_count}, 失败: {fail_count})")
            else:
                fail_count += 1
                print(f"⚠️  第 {i} 条数据返回空ID")
            
            # 简单的限流：每个请求间隔 200ms
            time.sleep(0.2)
                
        except Exception as e:
            fail_count += 1
            print(f"❌ 第 {i} 条数据创建失败: {str(e)[:80]}")
    
    print("\n" + "=" * 70)
    print(f"✅ 活动数据生成完成！")
    print(f"   总数: {count}")
    print(f"   成功: {success_count}")
    print(f"   失败: {fail_count}")
    if count > 0:
        print(f"   成功率: {(success_count/count)*100:.1f}%")
    
    # 验证数据
    try:
        total = EventModel.get_event_count()
        print(f"\n📊 数据库中活动总数: {total}")
        
        statuses = {}
        for status in ['计划中', '报名中', '进行中', '已完成', '已取消']:
            count = len(EventModel.list_by_status(status))
            if count > 0:
                statuses[status] = count
        
        if statuses:
            print(f"   按状态分布:")
            for status, count in statuses.items():
                print(f"     - {status}: {count}")
            
    except Exception as e:
        print(f"❌ 验证失败: {e}")

if __name__ == "__main__":
    batch_create_events(50)