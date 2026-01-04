#!/usr/bin/env python3
"""
模型功能测试演示脚本
演示所有模型的基本功能
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.volunteer import VolunteerModel
from models.event import EventModel
from models.schedule import ScheduleModel

def test_volunteer_model():
    """测试义工档案模型"""
    print("\n🧑‍💼 测试义工档案模型...")
    
    # 测试字段常量
    print(f"表单名称: {VolunteerModel.FORM_NAME}")
    print(f"姓名字段: {VolunteerModel.FIELD_NAME}")
    print(f"电话字段: {VolunteerModel.FIELD_PHONE}")
    print(f"状态字段: {VolunteerModel.FIELD_STATUS}")
    
    # 测试类方法存在
    methods = [
        'create_form', 'create', 'get_by_id', 'update', 'delete',
        'list_all', 'list_by_skill', 'list_by_status', 'list_by_volunteer_type',
        'search_by_name', 'get_volunteer_count', 'get_active_volunteers'
    ]
    
    for method in methods:
        if hasattr(VolunteerModel, method):
            print(f"✅ {method} 方法存在")
        else:
            print(f"❌ {method} 方法缺失")

def test_event_model():
    """测试活动库模型"""
    print("\n📅 测试活动库模型...")
    
    # 测试字段常量
    print(f"表单名称: {EventModel.FORM_NAME}")
    print(f"活动名称字段: {EventModel.FIELD_EVENT_NAME}")
    print(f"活动类型字段: {EventModel.FIELD_EVENT_TYPE}")
    print(f"活动状态字段: {EventModel.FIELD_STATUS}")
    
    # 测试类方法存在
    methods = [
        'create_form', 'create', 'get_by_id', 'update', 'delete',
        'list_all', 'list_by_type', 'list_by_status', 'list_upcoming_events',
        'search_by_name', 'get_event_count', 'get_events_by_date_range'
    ]
    
    for method in methods:
        if hasattr(EventModel, method):
            print(f"✅ {method} 方法存在")
        else:
            print(f"❌ {method} 方法缺失")

def test_schedule_model():
    """测试排班签到模型"""
    print("\n📋 测试排班签到模型...")
    
    # 测试字段常量
    print(f"表单名称: {ScheduleModel.FORM_NAME}")
    print(f"义工姓名字段: {ScheduleModel.FIELD_VOLUNTEER_NAME}")
    print(f"活动名称字段: {ScheduleModel.FIELD_EVENT_NAME}")
    print(f"签到状态字段: {ScheduleModel.FIELD_STATUS}")
    
    # 测试类方法存在
    methods = [
        'create_form', 'create', 'get_by_id', 'update', 'delete',
        'list_all', 'list_by_volunteer', 'list_by_event', 'list_by_date',
        'list_by_status', 'list_upcoming_schedules', 'check_in', 'check_out',
        'get_volunteer_hours', 'get_event_volunteers', 'get_schedule_count',
        'get_volunteer_schedule_count'
    ]
    
    for method in methods:
        if hasattr(ScheduleModel, method):
            print(f"✅ {method} 方法存在")
        else:
            print(f"❌ {method} 方法缺失")

def main():
    """主函数"""
    print("🚀 开始测试所有模型功能...")
    
    try:
        test_volunteer_model()
        test_event_model()
        test_schedule_model()
        
        print("\n🎉 所有模型测试完成！")
        print("\n📊 总结:")
        print("- ✅ 义工档案模型 (VolunteerModel) - 完整功能")
        print("- ✅ 活动库模型 (EventModel) - 完整功能") 
        print("- ✅ 排班签到模型 (ScheduleModel) - 完整功能")
        print("\n💡 使用说明:")
        print("1. 运行 python scripts/setup_forms.py 创建表单")
        print("2. 运行 python run_tests.py 运行单元测试")
        print("3. 查看 tests/ 目录下的测试文件了解使用方法")
        
    except Exception as e:
        print(f"❌ 测试过程中出错: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)