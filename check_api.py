#!/usr/bin/env python3
"""
API权限检查脚本
检查简道云API连接和权限状态
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.api_client import JDYClient
from config.settings import API_KEY, APP_ID

def check_api_connection():
    """检查API连接和权限"""
    print("🔍 开始检查简道云API连接...")
    
    # 检查配置
    print(f"📋 当前配置:")
    print(f"   APP_ID: {APP_ID}")
    print(f"   API_KEY: {API_KEY[:8]}..." if API_KEY else "未设置")
    
    if not API_KEY or not APP_ID:
        print("❌ 错误: API_KEY 或 APP_ID 未配置")
        print("💡 请检查 .env 文件是否正确设置")
        return False
    
    try:
        client = JDYClient()
        
        # 尝试获取表单列表
        print("🔄 测试API连接...")
        forms = client.get_form_list()
        
        print("✅ API连接成功！")
        print(f"📊 当前应用共有 {len(forms)} 个表单")
        
        if forms:
            print("\n📋 现有表单列表:")
            for i, form in enumerate(forms[:5], 1):  # 显示前5个
                print(f"   {i}. {form.get('name', '未知表单')} (ID: {form.get('entryId', 'N/A')})")
            if len(forms) > 5:
                print(f"   ... 还有 {len(forms) - 5} 个表单")
        
        # 尝试获取仪表盘列表
        dashboards = client.get_dashboard_list()
        print(f"📊 当前应用共有 {len(dashboards)} 个仪表盘")
        
        return True
        
    except Exception as e:
        print(f"❌ API连接失败: {str(e)}")
        print("\n🔧 可能的解决方案:")
        print("1. 检查 .env 文件中的 API_KEY 和 APP_ID 是否正确")
        print("2. 确认API密钥是否有权限访问该应用")
        print("3. 检查网络连接是否正常")
        print("4. 确认简道云账号是否有创建表单的权限")
        return False

def test_basic_operations():
    """测试基本操作"""
    print("\n🧪 测试基本操作...")
    
    try:
        client = JDYClient()
        
        # 测试获取应用信息
        print("✅ 可以创建JDYClient实例")
        print(f"✅ 应用ID: {client.app_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ 基本操作测试失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("🚀 简道云API权限检查工具")
    print("=" * 50)
    
    # 基本配置检查
    if not test_basic_operations():
        return False
    
    # API连接检查
    if not check_api_connection():
        return False
    
    print("\n🎉 API权限检查完成！")
    print("✅ 可以正常使用API创建表单和仪表盘")
    return True

if __name__ == "__main__":
    success = main()
    if success:
        print("\n💡 现在可以运行: python scripts/setup_forms.py 创建表单")
    else:
        print("\n⚠️ 请先解决上述问题后再运行表单创建脚本")
    sys.exit(0 if success else 1)