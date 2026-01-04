#!/usr/bin/env python3
"""
快速验证脚本
检查环境配置、模块导入、API连接是否正常
"""
import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def check_environment():
    """检查环境配置"""
    print("🔍 检查环境配置...")
    
    try:
        from config.settings import API_KEY, APP_ID
        
        if not API_KEY or not APP_ID:
            print("❌ 环境变量未配置")
            print("   请检查 .env 文件是否存在且包含：")
            print("   JDY_API_KEY=你的API密钥")
            print("   JDY_APP_ID=你的应用ID")
            return False
        
        print(f"✅ API_KEY: {API_KEY[:8]}...")
        print(f"✅ APP_ID: {APP_ID}")
        return True
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        print("   解决方案：")
        print("   1. 检查 .env 文件是否存在")
        print("   2. 运行: cp .env.example .env")
        print("   3. 编辑 .env 文件，填入正确的密钥")
        return False

def check_imports():
    """检查模块导入"""
    print("\n🔍 检查模块导入...")
    
    modules = [
        ("config.settings", "配置模块"),
        ("core.api_client", "API客户端"),
        ("models.volunteer", "义工模型"),
        ("models.event", "活动模型"),
        ("models.schedule", "排班模型"),
    ]
    
    all_ok = True
    for module_path, module_name in modules:
        try:
            __import__(module_path)
            print(f"✅ {module_name}")
        except Exception as e:
            print(f"❌ {module_name}: {e}")
            all_ok = False
    
    return all_ok

def check_api_connection():
    """检查API连接"""
    print("\n🔍 检查API连接...")
    
    try:
        from core.api_client import JDYClient
        
        client = JDYClient()
        forms = client.get_form_list()
        
        print(f"✅ API连接成功")
        print(f"✅ 找到 {len(forms)} 个表单")
        
        if forms:
            print(f"   已有表单示例：")
            for form in forms[:3]:
                form_name = form.get('name', '未知')
                form_id = form.get('entryId', 'N/A')
                print(f"     - {form_name} ({form_id})")
            if len(forms) > 3:
                print(f"     ... 还有 {len(forms) - 3} 个表单")
        
        return True
    except Exception as e:
        print(f"❌ API连接失败: {e}")
        print("\n   常见原因和解决方案：")
        print("   1. API密钥错误")
        print("      → 登录 https://www.jiandaoyun.com")
        print("      → 账户设置 → API密钥")
        print("      → 复制新密钥到 .env 文件")
        print("")
        print("   2. APP_ID错误")
        print("      → 在应用URL中查看：https://www.jiandaoyun.com/app/APP_ID")
        print("      → 复制 APP_ID 到 .env 文件")
        print("")
        print("   3. 网络问题")
        print("      → 检查网络连接是否正常")
        print("")
        print("   4. API权限不足")
        print("      → 确保API密钥有创建表单的权限")
        print("      → 确保应用没有设置为私有")
        return False

def check_files():
    """检查关键文件是否存在"""
    print("\n🔍 检查项目文件...")
    
    files = [
        ".env",
        "config/settings.py",
        "core/api_client.py",
        "models/volunteer.py",
        "models/event.py",
        "models/schedule.py",
        "scripts/init_system.py",
        "README.md",
        "requirements.txt",
    ]
    
    all_exist = True
    for file_path in files:
        exists = os.path.exists(file_path)
        status = "✅" if exists else "❌"
        print(f"{status} {file_path}")
        if not exists:
            all_exist = False
    
    return all_exist

def main():
    """主函数"""
    print("🚀 义工管理系统快速检查")
    print("=" * 60)
    
    checks = [
        ("文件检查", check_files),
        ("环境配置", check_environment),
        ("模块导入", check_imports),
        ("API连接", check_api_connection),
    ]
    
    results = {}
    for check_name, check_func in checks:
        try:
            result = check_func()
            results[check_name] = result
        except Exception as e:
            print(f"\n❌ {check_name} 检查异常: {e}")
            results[check_name] = False
    
    print("\n" + "=" * 60)
    print("📊 检查结果汇总：")
    print("=" * 60)
    
    for check_name, result in results.items():
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{status}: {check_name}")
    
    print("\n" + "=" * 60)
    
    if all(results.values()):
        print("🎉 所有检查通过！系统正常")
        print("\n✨ 下一步操作：")
        print("  1. 初始化系统表单:")
        print("     python scripts/init_system.py")
        print("")
        print("  2. 在简道云后台查看创建的表单")
        print("")
        print("  3. 开始使用：")
        print("     from models.volunteer import VolunteerModel")
        print("     VolunteerModel.list_all()")
        return True
    else:
        print("⚠️  有些检查失败，请查看上述错误信息")
        print("\n💡 常见问题：")
        print("  • .env 文件不存在？运行: cp .env.example .env")
        print("  • 找不到模块？运行: pip install -r requirements.txt")
        print("  • API连接失败？检查 .env 中的密钥是否正确")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)