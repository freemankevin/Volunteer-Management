#!/usr/bin/env python3
"""
表单配置验证脚本
验证简道云表单是否正确配置
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.api_client import JDYClient
from config.settings import (
    API_KEY, APP_ID,
    VOLUNTEER_ENTRY_ID, EVENT_ENTRY_ID, SCHEDULE_ENTRY_ID
)

def verify_forms():
    """验证三个核心表单是否存在且配置正确"""
    print("🔧 简道云表单配置验证")
    print("=" * 60)
    
    print(f"✅ API_KEY: {API_KEY[:12]}...")
    print(f"✅ APP_ID: {APP_ID}")
    
    client = JDYClient()
    
    forms_config = [
        ("义工档案表", VOLUNTEER_ENTRY_ID),
        ("活动库表", EVENT_ENTRY_ID),
        ("排班签到表", SCHEDULE_ENTRY_ID),
    ]
    
    print("\n📋 验证表单配置...")
    all_ok = True
    
    for form_name, entry_id in forms_config:
        try:
            result = client.get_form_widgets(entry_id)
            widgets = result.get('widgets', [])
            field_count = len(widgets)
            
            print(f"✅ {form_name} (ENTRY_ID: {entry_id[:8]}...) - 找到 {field_count} 个字段")
                
        except Exception as e:
            print(f"❌ {form_name} (ENTRY_ID: {entry_id[:8]}...) - 验证失败: {str(e)[:50]}")
            all_ok = False
    
    print("\n" + "=" * 60)
    if all_ok:
        print("🎉 所有表单配置正确！可以开始使用系统了。")
        print("\n下一步：")
        print("  from models.volunteer import VolunteerModel")
        print("  VolunteerModel.create(name='张三', phone='13800138000', age=35)")
        return True
    else:
        print("❌ 部分表单配置有问题")
        print("\n解决方案：")
        print("  1. 检查 .env 文件中的 ENTRY_ID 是否正确")
        print("  2. 确保在简道云后台已创建对应的表单")
        return False

if __name__ == "__main__":
    try:
        success = verify_forms()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 验证过程出错: {e}")
        sys.exit(1)