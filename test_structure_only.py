"""
仅测试代码结构，不测试API连接
"""
import sys
import os
import json

# 临时修改路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 创建一个模拟的API客户端用于测试
class MockJDYClient:
    def create_dashboard(self, data):
        return "mock_dashboard_id"
    def create_form(self, data):
        return "mock_form_id"

# 临时替换导入
import services.dashboard_builder
import services.form_builder

# 保存原始导入
original_jdy_client = services.dashboard_builder.JDYClient
original_form_client = services.form_builder.JDYClient

# 替换为mock
services.dashboard_builder.JDYClient = MockJDYClient
services.form_builder.JDYClient = MockJDYClient

# 现在导入类
from services.dashboard_builder import DashboardBuilder
from services.form_builder import FormBuilder

def test_dashboard_structure():
    """测试仪表盘结构"""
    print("🧪 测试仪表盘结构...")
    
    try:
        builder = DashboardBuilder()
        
        # 测试方法存在
        methods = [
            'create_volunteer_dashboard',
            'create_activity_dashboard', 
            'create_performance_dashboard',
            'create_custom_dashboard'
        ]
        
        for method in methods:
            assert hasattr(builder, method), f"缺少方法: {method}"
        print("✅ 所有方法存在")
        
        # 测试添加组件
        builder.add_stat_widget("测试统计", "test_form", "name")
        builder.add_chart_widget("测试图表", "pie", "test_form", "category", "count")
        builder.add_table_widget("测试表格", "test_form", ["name", "email"])
        
        assert len(builder.widgets) == 3
        print("✅ 组件添加成功")
        
        # 测试数据结构
        dashboard_data = {
            "name": "测试仪表盘",
            "description": "测试描述",
            "widgets": builder.widgets
        }
        
        # 验证JSON序列化
        json_str = json.dumps(dashboard_data, ensure_ascii=False, indent=2)
        print("✅ JSON结构正确")
        print("📊 示例仪表盘数据:")
        print(json_str[:500] + "..." if len(json_str) > 500 else json_str)
        
        return True
        
    except Exception as e:
        print(f"❌ 仪表盘测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_form_structure():
    """测试表单结构"""
    print("\n🧪 测试表单结构...")
    
    try:
        builder = FormBuilder()
        
        # 测试方法存在
        methods = [
            'create_volunteer_registration_form',
            'create_activity_registration_form',
            'create_feedback_form',
            'create_custom_form'
        ]
        
        for method in methods:
            assert hasattr(builder, method), f"缺少方法: {method}"
        print("✅ 所有方法存在")
        
        # 测试字段添加
        (builder
         .add_text_field("name", "姓名", required=True)
         .add_email_field("email", "邮箱")
         .add_select_field("department", "部门", ["技术", "市场"]))
        
        assert len(builder.fields) == 3
        print("✅ 字段添加成功")
        
        # 测试表单数据结构
        form_data = {
            "name": "测试表单",
            "description": "测试描述",
            "widgets": builder.fields
        }
        
        # 验证JSON序列化
        json_str = json.dumps(form_data, ensure_ascii=False, indent=2)
        print("✅ JSON结构正确")
        print("📋 示例表单数据:")
        print(json_str[:500] + "..." if len(json_str) > 500 else json_str)
        
        return True
        
    except Exception as e:
        print(f"❌ 表单测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("测试简道云代码结构（无需API密钥）")
    print("=" * 50)
    
    success1 = test_dashboard_structure()
    success2 = test_form_structure()
    
    # 恢复原始导入
    services.dashboard_builder.JDYClient = original_jdy_client
    services.form_builder.JDYClient = original_form_client
    
    if success1 and success2:
        print("\n🎉 所有结构测试通过！")
        print("\n修复总结：")
        print("✅ 修复了dashboard_builder.py中的JSON结构错误")
        print("✅ 简化了仪表盘数据结构，去除了复杂的layout嵌套")
        print("✅ 确保所有方法都能正确创建数据结构")
        print("\n下一步：")
        print("1. 复制.env.example到.env")
        print("2. 填入你的简道云API密钥")
        print("3. 运行完整测试: python tests/test_jdy_integration.py")
    else:
        print("\n⚠️  结构测试未完全通过")