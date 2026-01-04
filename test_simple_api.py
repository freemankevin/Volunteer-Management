#!/usr/bin/env python3
"""
简化的API测试脚本
"""
import sys
import os
import requests
import time
import hashlib

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_simple_connection():
    """测试简化的API连接"""
    try:
        from config.settings import API_KEY, APP_ID
        
        print("🔍 测试简道云API连接...")
        print(f"APP_ID: {APP_ID}")
        print(f"API_KEY: {API_KEY[:8]}..." if API_KEY else "未设置")
        
        if not API_KEY or not APP_ID:
            print("❌ API_KEY 或 APP_ID 未设置")
            return False
        
        # 简道云API端点
        base_url = "https://api.jiandaoyun.com/api/v5"
        
        # 生成签名
        timestamp = str(int(time.time() * 1000))
        sign_str = f'{API_KEY}{timestamp}'
        signature = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
        
        headers = {
            'Content-Type': 'application/json',
            'X-Api-Key': API_KEY,
            'X-Timestamp': timestamp,
            'X-Sign': signature
        }
        
        # 测试获取表单列表
        url = f"{base_url}/app/{APP_ID}/entry"
        print(f"🔄 测试: {url}")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"📊 状态码: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('code') == 0:
                    print("✅ API连接成功！")
                    forms = data.get('data', [])
                    print(f"📋 找到 {len(forms)} 个表单")
                    return True
                else:
                    print(f"❌ API错误: {data.get('msg', '未知错误')}")
                    return False
            except Exception as e:
                print(f"❌ JSON解析错误: {e}")
                return False
        else:
            print(f"❌ HTTP错误: {response.status_code}")
            print(f"响应: {response.text[:200]}...")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_simple_connection()
    if success:
        print("\n✅ API连接正常，可以创建表单")
    else:
        print("\n❌ 需要检查API配置")
    sys.exit(0 if success else 1)