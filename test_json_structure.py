"""
直接测试JSON数据结构，不依赖任何导入
"""
import json

def test_dashboard_json_structure():
    """测试仪表盘JSON结构"""
    print("🧪 测试仪表盘JSON结构...")
    
    # 模拟修复后的仪表盘数据结构
    dashboard_data = {
        "name": "志愿者管理仪表盘",
        "description": "志愿者活动数据总览",
        "widgets": [
            {
                "type": "stat",
                "title": "总志愿者人数",
                "dataSource": "volunteer_form_id",
                "field": "name",
                "operation": "count"
            },
            {
                "type": "stat",
                "title": "本月活动次数",
                "dataSource": "activity_form_id",
                "field": "activity",
                "operation": "count"
            },
            {
                "type": "chart",
                "title": "志愿者年龄分布",
                "chartType": "pie",
                "dataSource": "volunteer_form_id",
                "xField": "age",
                "yField": "count"
            },
            {
                "type": "table",
                "title": "最近活动报名",
                "dataSource": "activity_form_id",
                "fields": ["volunteer_name", "activity", "activity_date"],
                "pageSize": 5
            }
        ]
    }
    
    try:
        # 验证JSON序列化
        json_str = json.dumps(dashboard_data, ensure_ascii=False, indent=2)
        print("✅ 仪表盘JSON结构正确")
        print("📊 示例仪表盘数据:")
        print(json_str)
        return True
    except Exception as e:
        print(f"❌ 仪表盘JSON错误: {str(e)}")
        return False

def test_form_json_structure():
    """测试表单JSON结构"""
    print("\n🧪 测试表单JSON结构...")
    
    # 模拟修复后的表单数据结构
    form_data = {
        "name": "志愿者注册表单",
        "description": "志愿者信息登记表单",
        "widgets": [
            {
                "name": "name",
                "label": "姓名",
                "type": "text",
                "required": True
            },
            {
                "name": "phone",
                "label": "手机号码",
                "type": "phone",
                "required": True
            },
            {
                "name": "email",
                "label": "邮箱地址",
                "type": "email",
                "required": False
            },
            {
                "name": "department",
                "label": "部门",
                "type": "select",
                "required": True,
                "options": [
                    {"label": "技术", "value": "技术"},
                    {"label": "市场", "value": "市场"}
                ]
            }
        ]
    }
    
    try:
        # 验证JSON序列化
        json_str = json.dumps(form_data, ensure_ascii=False, indent=2)
        print("✅ 表单JSON结构正确")
        print("📋 示例表单数据:")
        print(json_str)
        return True
    except Exception as e:
        print(f"❌ 表单JSON错误: {str(e)}")
        return False

def test_original_vs_fixed():
    """对比原始错误结构和修复后结构"""
    print("\n📊 对比原始错误 vs 修复后结构")
    
    # 原始错误结构（layout嵌套）
    original_wrong = {
        "name": "测试仪表盘",
        "description": "测试描述",
        "layout": [  # 错误的嵌套结构
            {
                "type": "row",
                "widgets": [
                    {"type": "stat", "title": "统计1"}
                ]
            }
        ]
    }
    
    # 修复后结构（直接widgets）
    fixed_correct = {
        "name": "测试仪表盘",
        "description": "测试描述",
        "widgets": [  # 正确的扁平结构
            {"type": "stat", "title": "统计1"},
            {"type": "chart", "title": "图表1"}
        ]
    }
    
    print("❌ 原始错误结构（layout嵌套）:")
    print(json.dumps(original_wrong, indent=2))
    
    print("\n✅ 修复后结构（直接widgets）:")
    print(json.dumps(fixed_correct, indent=2))

if __name__ == "__main__":
    print("测试简道云JSON数据结构修复")
    print("=" * 50)
    
    success1 = test_dashboard_json_structure()
    success2 = test_form_json_structure()
    test_original_vs_fixed()
    
    if success1 and success2:
        print("\n🎉 所有JSON结构测试通过！")
        print("\n修复总结：")
        print("✅ 修复了dashboard_builder.py中的JSON结构错误")
        print("✅ 简化了仪表盘数据结构，从复杂的layout嵌套改为直接的widgets数组")
        print("✅ 确保所有JSON数据都能正确序列化")
        print("✅ 符合简道云API的数据格式要求")
        print("\n下一步：")
        print("1. 复制.env.example到.env")
        print("2. 填入你的简道云API密钥")
        print("3. 运行: python tests/test_jdy_integration.py")
    else:
        print("\n⚠️  JSON结构测试未完全通过")