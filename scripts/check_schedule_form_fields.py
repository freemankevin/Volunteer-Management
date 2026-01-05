#!/usr/bin/env python3
"""
检查排班签到表中实际存在的字段
"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.api_client import JDYClient
from config.settings import SCHEDULE_ENTRY_ID

def check_schedule_fields():
    """检查排班签到表的字段"""
    client = JDYClient()
    
    print("🔍 检查排班签到表的字段...\n")
    
    try:
        result = client.get_form_widgets(SCHEDULE_ENTRY_ID)
        
        widgets = result.get('widgets', [])
        
        if not widgets:
            print("❌ 没有找到任何字段！表单可能是空的。")
            return False
        
        print(f"找到 {len(widgets)} 个字段:\n")
        print("=" * 80)
        
        for i, widget in enumerate(widgets, 1):
            field_name = widget.get('label', 'Unknown')
            field_type = widget.get('type', 'Unknown')
            field_id = widget.get('name', 'Unknown')
            
            print(f"{i}. 字段名称: {field_name}")
            print(f"   Widget ID: {field_id}")
            print(f"   字段类型: {field_type}")
            print()
        
        print("=" * 80)
        print("\n💡 Python 代码映射（复制到 models/schedule.py）：\n")
        print("```python")
        for widget in widgets:
            field_label = widget.get('label', 'Unknown')
            field_id = widget.get('name', 'Unknown')
            # 转换字段名为常量形式
            constant_name = 'FIELD_' + field_label.upper().replace(' ', '_').replace('（', '').replace('）', '')
            print(f"{constant_name} = \"{field_id}\"")
        print("```")
        
        print("\n✅ 字段检查完毕！")
        return True
        
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 80)
    print("📋 排班签到表字段检查工具")
    print("=" * 80 + "\n")
    
    check_schedule_fields()