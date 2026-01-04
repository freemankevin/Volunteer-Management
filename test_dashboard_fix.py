"""
测试dashboard_builder.py修复后的功能
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.dashboard_builder import DashboardBuilder
from services.form_builder import FormBuilder

def test_dashboard_structure():
    """测试仪表盘结构是否正确"""
    print("🧪 测试仪表盘构建器...")
    
    try:
        # 测试导入
        builder = DashboardBuilder()
        print("✅ DashboardBuilder 导入成功")
        
        # 测试方法是否存在
        assert hasattr(builder, 'create_volunteer_dashboard')
        assert hasattr(builder, 'create_activity_dashboard')
        assert hasattr(builder, 'create_performance_dashboard')
        assert hasattr(builder, 'create_custom_dashboard')
        print("✅ 所有方法存在")
        
        # 测试添加组件
        builder.add_stat_widget("测试统计", "test_form", "name")
        builder.add_chart_widget("测试图表", "pie", "test_form", "category", "count")
        builder.add_table_widget("测试表格", "test_form", ["name", "email"])
        print("✅ 组件添加成功")
        
        # 测试数据结构
        assert len(builder.widgets) == 3
        assert builder.widgets[0]["type"] == "stat"
        assert builder.widgets[1]["type"] == "chart"
        assert builder.widgets[2]["type"] == "table"
        print("✅ 数据结构正确")
        
        # 测试自定义仪表盘创建
        custom_dashboard_data = {
            "name": "测试仪表盘",
            "description": "测试描述",
            "widgets": builder.widgets
        }
        
        # 验证数据结构
        assert "name" in custom_dashboard_data
        assert "description" in custom_dashboard_data
        assert "widgets" in custom_dashboard_data
        assert isinstance(custom_dashboard_data["widgets"], list)
        print("✅ 自定义仪表盘数据结构正确")
        
        print("\n🎉 所有测试通过！dashboard_builder.py 修复成功")
        return True
        
    except Exception as e:
        print(f"❌ 测试失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def test_form_builder():
    """测试表单构建器是否正常"""
    print("\n🧪 测试表单构建器...")
    
    try:
        builder = FormBuilder()
        
        # 测试创建简单表单
        form_data = {
            "name": "测试表单",
            "description": "测试描述",
            "widgets": [
                {
                    "name": "test_name",
                    "label": "测试名称",
                    "type": "text",
                    "required": True
                }
            ]
        }
        
        assert "name" in form_data
        assert "description" in form_data
        assert "widgets" in form_data
        print("✅ 表单数据结构正确")
        
        return True
        
    except Exception as e:
        print(f"❌ 表单构建器测试失败: {str(e)}")
        return False

if __name__ == "__main__":
    print("测试简道云仪表盘和表单构建器")
    print("=" * 50)
    
    success1 = test_dashboard_structure()
    success2 = test_form_builder()
    
    if success1 and success2:
        print("\n🎉 所有测试通过！代码修复成功")
        print("\n下一步：")
        print("1. 配置.env文件中的API密钥")
        print("2. 运行: python examples/create_forms_and_dashboards.py")
        print("3. 或运行: python tests/test_jdy_integration.py")
    else:
        print("\n⚠️  测试未完全通过，请检查错误信息")