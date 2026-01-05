#!/usr/bin/env python3
"""
检查表单中实际存在的字段
"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.api_client import JDYClient
from config.settings import VOLUNTEER_ENTRY_ID

def check_volunteer_fields():
    """检查义工表的字段"""
    client = JDYClient()
    
    print("🔍 检查义工档案表的字段...\n")
    
    try:
        result = client.get_form_widgets(VOLUNTEER_ENTRY_ID)
        
        widgets = result.get('widgets', [])
        
        if not widgets:
            print("❌ 没有找到任何字段！表单可能是空的。")
            print("\n需要在简道云后台手动创建字段。")
            return
        
        print(f"找到 {len(widgets)} 个字段:\n")
        print("字段列表:")
        print("-" * 60)
        
        for widget in widgets:
            field_name = widget.get('name', 'Unknown')
            field_type = widget.get('type', 'Unknown')
            field_id = widget.get('id', 'Unknown')
            
            print(f"名称: {field_name}")
            print(f"  类型: {field_type}")
            print(f"  ID:   {field_id}")
            print()
        
        print("-" * 60)
        print("\n✅ 使用这些字段名进行数据创建")
        
    except Exception as e:
        print(f"❌ 查询失败: {e}")

if __name__ == "__main__":
    check_volunteer_fields()