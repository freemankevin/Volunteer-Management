# scripts/init_system.py
#!/usr/bin/env python3
"""初始化系统 - 创建三个核心表单"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.api_client import JDYClient

def create_forms():
    """创建三个核心表单"""
    client = JDYClient()
    
    # 表单1: 义工档案
    volunteer_form = {
        "name": "义工档案",
        "widgets": [
            {"type": "text", "name": "name", "label": "姓名", "required": True},
            {"type": "phone", "name": "phone", "label": "手机号", "required": True},
            {"type": "number", "name": "age", "label": "年龄", "min": 16, "max": 80},
            {"type": "select", "name": "gender", "label": "性别", "options": ["男", "女"]},
            {"type": "textarea", "name": "skills", "label": "技能特长"},
            {"type": "select", "name": "status", "label": "状态", 
             "options": ["活跃", "暂停", "退出"], "default": "活跃"},
        ]
    }
    
    # 表单2: 活动库
    event_form = {
        "name": "活动库",
        "widgets": [
            {"type": "text", "name": "event_name", "label": "活动名称", "required": True},
            {"type": "date", "name": "event_date", "label": "活动日期", "required": True},
            {"type": "time", "name": "start_time", "label": "开始时间", "required": True},
            {"type": "time", "name": "end_time", "label": "结束时间", "required": True},
            {"type": "text", "name": "location", "label": "活动地点", "required": True},
            {"type": "number", "name": "volunteers_needed", "label": "需要义工人数"},
            {"type": "select", "name": "status", "label": "活动状态",
             "options": ["计划中", "报名中", "进行中", "已完成", "已取消"], "default": "计划中"},
        ]
    }
    
    # 表单3: 排班签到
    schedule_form = {
        "name": "排班签到",
        "widgets": [
            {"type": "text", "name": "volunteer_name", "label": "义工姓名", "required": True},
            {"type": "phone", "name": "volunteer_phone", "label": "义工电话", "required": True},
            {"type": "text", "name": "event_name", "label": "活动名称", "required": True},
            {"type": "date", "name": "event_date", "label": "活动日期", "required": True},
            {"type": "select", "name": "role", "label": "担任角色",
             "options": ["负责人", "协助人", "接待员", "清洁员", "摄影员", "其他"]},
            {"type": "select", "name": "status", "label": "签到状态",
             "options": ["已排班", "已确认", "已签到", "已签退", "缺席"],
             "default": "已排班"},
            {"type": "number", "name": "hours", "label": "工时", "min": 0, "max": 24},
        ]
    }
    
    try:
        print("🚀 开始创建表单...")
        
        v_id = client.create_form(volunteer_form)
        print(f"✅ 义工档案表单: {v_id}")
        
        e_id = client.create_form(event_form)
        print(f"✅ 活动库表单: {e_id}")
        
        s_id = client.create_form(schedule_form)
        print(f"✅ 排班签到表单: {s_id}")
        
        print("\n🎉 系统初始化完成！")
        print(f"保存这些ID供后续使用：")
        print(f"  VOLUNTEER_FORM_ID={v_id}")
        print(f"  EVENT_FORM_ID={e_id}")
        print(f"  SCHEDULE_FORM_ID={s_id}")
        
        return True
    except Exception as e:
        print(f"❌ 创建表单失败: {e}")
        return False

if __name__ == "__main__":
    success = create_forms()
    sys.exit(0 if success else 1)


# ========================================
# quick_check.py - 快速验证脚本
# ========================================
#!/usr/bin/env python3
"""快速验证系统是否正常"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境...")
    
    try:
        from config.settings import API_KEY, APP_ID
        
        if not API_KEY or not APP_ID:
            print("❌ 环境变量未配置")
            return False
        
        print(f"✅ API_KEY: {API_KEY[:8]}...")
        print(f"✅ APP_ID: {APP_ID}")
        return True
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False

def check_imports():
    """检查模块导入"""
    print("\n🔍 检查模块导入...")
    
    try:
        from core.api_client import JDYClient
        from models.volunteer import VolunteerModel
        from models.event import EventModel
        from models.schedule import ScheduleModel
        
        print("✅ core.api_client")
        print("✅ models.volunteer")
        print("✅ models.event")
        print("✅ models.schedule")
        return True
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        return False

def check_api_connection():
    """检查API连接"""
    print("\n🔍 检查API连接...")
    
    try:
        from core.api_client import JDYClient
        
        client = JDYClient()
        forms = client.get_form_list()
        
        print(f"✅ API连接成功，找到 {len(forms)} 个表单")
        return True
    except Exception as e:
        print(f"❌ API连接失败: {e}")
        print("   检查: .env 文件中的API密钥和APP_ID是否正确")
        return False

def main():
    print("🚀 义工管理系统快速检查\n" + "="*50)
    
    checks = [
        ("环境配置", check_environment),
        ("模块导入", check_imports),
        ("API连接", check_api_connection),
    ]
    
    results = []
    for name, check_func in checks:
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"❌ {name} 检查异常: {e}")
            results.append(False)
    
    print("\n" + "="*50)
    if all(results):
        print("🎉 所有检查通过！系统正常")
        print("\n下一步:")
        print("  1. python scripts/init_system.py  # 创建表单")
        print("  2. 在简道云后台查看创建的表单")
        return True
    else:
        print("⚠️  有些检查失败，请上述错误信息")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)