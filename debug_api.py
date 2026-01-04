#!/usr/bin/env python3
"""
API调试脚本
用于测试简道云API连接和权限
"""
import sys
import os
import requests
import time
import hashlib

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_api_direct():
    """直接测试API连接"""
    from config.settings import API_KEY, APP_ID
    
    print("🔍 直接测试简道云API连接...")
    print(f"APP_ID: {APP_ID}")
    print(f"API_KEY: {API_KEY[:8]}..." if API_KEY else "未设置")
    
    if not API_KEY or not APP_ID:
        print("❌ API_KEY 或 APP_ID 未设置")
        return False
    
    # 简道云API的正确端点
    base_url = "https://api.jiandaoyun.com/api/v1"
    
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
    
    try:
        # 测试获取应用信息
        url = f"{base_url}/app/{APP_ID}/entry"
        print(f"🔄 测试端点: {url}")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"📊 响应状态码: {response.status_code}")
        print(f"📊 响应内容: {response.text[:500]}...")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("✅ API连接成功！")
                print(f"📋 响应数据: {data}")
                return True
            except:
                print("❌ 响应不是有效的JSON格式")
                return False
        else:
            print(f"❌ API请求失败: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        return False

def test_with_correct_endpoint():
    """使用正确的简道云API端点测试"""
    from config.settings import API_KEY, APP_ID
    
    print("\n🔍 使用简道云v5 API测试...")
    
    # 简道云v5 API端点
    base_url = "https://api.jiandaoyun.com/api/v5"
    
    # 生成签名
    timestamp = str(int(time.time() * 1000))
    sign_str = f'{API_KEY}{timestamp}'
    signature = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {API_KEY}',
        'X-Timestamp': timestamp,
        'X-Sign': signature
    }
    
    try:
        # 测试获取表单列表
        url = f"{base_url}/app/{APP_ID}/form"
        print(f"🔄 测试端点: {url}")
        
        response = requests.get(url, headers=headers, timeout=10)
        
        print(f"📊 响应状态码: {response.status_code}")
        print(f"📊 响应内容: {response.text[:500]}...")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"❌ 请求异常: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 简道云API调试工具")
    print("=" * 50)
    
    # 测试直接API连接
    success1 = test_api_direct()
    
    # 测试v5 API
    success2 = test_with_correct_endpoint()
    
    print("\n📊 测试结果总结:")
    print(f"直接API测试: {'✅ 通过' if success1 else '❌ 失败'}")
    print(f"v5 API测试: {'✅ 通过' if success2 else '❌ 失败'}")
    
    return success1 or success2

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)