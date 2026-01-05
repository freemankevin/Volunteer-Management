#!/usr/bin/env python3
"""
调试活动库表字段 - 查看原始 API 响应
"""
import sys
import os
import json
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.api_client import JDYClient
from config.settings import EVENT_ENTRY_ID

def debug_event_fields():
    """调试活动库表的字段 - 显示原始 API 响应"""
    client = JDYClient()
    
    print("🔍 调试活动库表字段...\n")
    print("=" * 80)
    
    try:
        result = client.get_form_widgets(EVENT_ENTRY_ID)
        
        # 打印完整的原始响应
        print("📡 原始 API 响应：\n")
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
        print("\n" + "=" * 80)
        print("\n📊 字段解析：\n")
        
        widgets = result.get('widgets', [])
        
        if not widgets:
            print("❌ 没有找到任何字段！")
            return
        
        print(f"总共找到 {len(widgets)} 个字段\n")
        
        for i, widget in enumerate(widgets, 1):
            print(f"字段 #{i}:")
            print(f"  完整数据: {json.dumps(widget, indent=4, ensure_ascii=False)}")
            print()
        
    except Exception as e:
        print(f"❌ 查询失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=" * 80)
    print("🛠️  活动库表字段调试工具")
    print("=" * 80 + "\n")
    
    debug_event_fields()