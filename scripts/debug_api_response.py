#!/usr/bin/env python3
"""
调试API响应格式
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.api_client import JDYClient
from config.settings import VOLUNTEER_ENTRY_ID

def debug_create_response():
    """调试创建数据的响应"""
    client = JDYClient()
    
    test_data = {
        "姓名": "测试用户",
        "手机号": "13800000000",
        "年龄": 30,
        "性别": "男",
        "状态": "活跃"
    }
    
    print("=== 调试创建义工响应 ===\n")
    print(f"发送数据: {test_data}\n")
    
    try:
        # 直接调用API
        import json
        endpoint = "/app/entry/data/create"
        payload = {
            "app_id": client.app_id,
            "entry_id": VOLUNTEER_ENTRY_ID,
            "data": {key: {'value': value} for key, value in test_data.items()},
            "is_start_trigger": False,
            "is_start_workflow": False,
            "transaction_id": client._generate_transaction_id()
        }
        
        print(f"请求体:\n{json.dumps(payload, indent=2, ensure_ascii=False)}\n")
        
        result = client.request('POST', endpoint, payload)
        
        print(f"API 响应:\n{json.dumps(result, indent=2, ensure_ascii=False)}\n")
        
        # 检查各种可能的ID位置
        print("=== ID 检查 ===")
        print(f"result.get('_id'): {result.get('_id')}")
        print(f"result.get('data'): {result.get('data')}")
        if isinstance(result.get('data'), dict):
            print(f"result['data'].get('_id'): {result.get('data', {}).get('_id')}")
        print(f"result keys: {list(result.keys())}")
        
    except Exception as e:
        print(f"❌ 调试失败: {e}")

def debug_query_response():
    """调试查询数据的响应"""
    client = JDYClient()
    
    print("\n=== 调试查询义工响应 ===\n")
    
    try:
        endpoint = "/app/entry/data/list"
        payload = {
            "app_id": client.app_id,
            "entry_id": VOLUNTEER_ENTRY_ID,
            "limit": 1
        }
        
        result = client.request('POST', endpoint, payload)
        
        import json
        print(f"API 响应 (部分):\n{json.dumps(result, indent=2, ensure_ascii=False)[:500]}...\n")
        
        if isinstance(result.get('data'), list) and len(result['data']) > 0:
            first_record = result['data'][0]
            print(f"第一条记录的 keys: {list(first_record.keys())}")
            print(f"第一条记录的 _id: {first_record.get('_id')}")
        
    except Exception as e:
        print(f"❌ 调试失败: {e}")

if __name__ == "__main__":
    debug_create_response()
    debug_query_response()