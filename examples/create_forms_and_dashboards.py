"""
简道云表单和仪表盘创建示例
演示如何使用FormBuilder和DashboardBuilder创建完整的志愿者管理系统
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.form_builder import FormBuilder
from services.dashboard_builder import DashboardBuilder
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_complete_volunteer_system():
    """创建完整的志愿者管理系统"""
    
    print("🚀 开始创建志愿者管理系统...")
    
    # 初始化构建器
    form_builder = FormBuilder()
    dashboard_builder = DashboardBuilder()
    
    try:
        # 1. 创建表单
        print("📋 创建表单...")
        
        # 创建志愿者注册表单
        volunteer_form_id = form_builder.create_volunteer_registration_form()
        print(f"✅ 志愿者注册表单创建成功: {volunteer_form_id}")
        
        # 创建活动报名表单
        activity_form_id = form_builder.create_activity_registration_form()
        print(f"✅ 活动报名表单创建成功: {activity_form_id}")
        
        # 创建活动反馈表单
        feedback_form_id = form_builder.create_feedback_form()
        print(f"✅ 活动反馈表单创建成功: {feedback_form_id}")
        
        # 2. 创建仪表盘
        print("📊 创建仪表盘...")
        
        # 创建志愿者管理仪表盘
        volunteer_dashboard_id = dashboard_builder.create_volunteer_dashboard(
            volunteer_form_id, activity_form_id, feedback_form_id
        )
        print(f"✅ 志愿者管理仪表盘创建成功: {volunteer_dashboard_id}")
        
        # 创建活动管理仪表盘
        activity_dashboard_id = dashboard_builder.create_activity_dashboard(
            activity_form_id, feedback_form_id
        )
        print(f"✅ 活动管理仪表盘创建成功: {activity_dashboard_id}")
        
        # 创建绩效分析仪表盘
        performance_dashboard_id = dashboard_builder.create_performance_dashboard(
            volunteer_form_id, activity_form_id
        )
        print(f"✅ 绩效分析仪表盘创建成功: {performance_dashboard_id}")
        
        # 3. 输出结果
        print("\n🎉 系统创建完成！")
        print("=" * 50)
        print("表单ID:")
        print(f"  志愿者注册表单: {volunteer_form_id}")
        print(f"  活动报名表单: {activity_form_id}")
        print(f"  活动反馈表单: {feedback_form_id}")
        print("\n仪表盘ID:")
        print(f"  志愿者管理仪表盘: {volunteer_dashboard_id}")
        print(f"  活动管理仪表盘: {activity_dashboard_id}")
        print(f"  绩效分析仪表盘: {performance_dashboard_id}")
        print("=" * 50)
        
        return {
            "forms": {
                "volunteer_registration": volunteer_form_id,
                "activity_registration": activity_form_id,
                "feedback": feedback_form_id
            },
            "dashboards": {
                "volunteer_management": volunteer_dashboard_id,
                "activity_management": activity_dashboard_id,
                "performance_analysis": performance_dashboard_id
            }
        }
        
    except Exception as e:
        logger.error(f"创建系统时出错: {str(e)}")
        raise

def create_custom_form_example():
    """创建自定义表单示例"""
    
    print("📝 创建自定义表单示例...")
    
    form_builder = FormBuilder()
    
    # 创建自定义调查表单
    custom_form_id = (form_builder
                     .add_text_field("company", "公司名称", required=True)
                     .add_text_field("department", "部门", required=True)
                     .add_select_field("position", "职位", ["经理", "主管", "专员", "助理"], required=True)
                     .add_number_field("experience", "工作年限", required=True, min_value=0, max_value=50)
                     .add_select_field("satisfaction", "工作满意度", ["非常满意", "满意", "一般", "不满意"], required=True)
                     .add_textarea_field("suggestions", "改进建议")
                     .create_custom_form("员工满意度调查", "公司内部员工满意度调查表单"))
    
    print(f"✅ 自定义表单创建成功: {custom_form_id}")
    return custom_form_id

def create_custom_dashboard_example():
    """创建自定义仪表盘示例"""
    
    print("📈 创建自定义仪表盘示例...")
    
    dashboard_builder = DashboardBuilder()
    
    # 创建自定义仪表盘
    custom_dashboard_id = (dashboard_builder
                          .add_stat_widget("总调查人数", "form_xxx", "company")
                          .add_chart_widget("满意度分布", "pie", "form_xxx", "satisfaction", "count")
                          .add_chart_widget("工作年限分布", "bar", "form_xxx", "experience", "count")
                          .add_table_widget("最新反馈", "form_xxx", ["company", "satisfaction", "suggestions"], 10)
                          .create_custom_dashboard("员工满意度分析", "员工满意度调查数据分析"))
    
    print(f"✅ 自定义仪表盘创建成功: {custom_dashboard_id}")
    return custom_dashboard_id

def list_existing_forms_and_dashboards():
    """列出现有表单和仪表盘"""
    
    print("📋 列出现有表单和仪表盘...")
    
    client = FormBuilder().client
    
    try:
        # 获取表单列表
        forms = client.get_form_list()
        print("\n现有表单:")
        for form in forms:
            print(f"  - {form.get('name')} (ID: {form.get('entryId')})")
        
        # 获取仪表盘列表
        dashboards = client.get_dashboard_list()
        print("\n现有仪表盘:")
        for dashboard in dashboards:
            print(f"  - {dashboard.get('name')} (ID: {dashboard.get('dashboardId')})")
            
    except Exception as e:
        logger.error(f"获取列表时出错: {str(e)}")

if __name__ == "__main__":
    
    print("简道云表单和仪表盘创建工具")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 创建完整的志愿者管理系统")
        print("2. 创建自定义表单示例")
        print("3. 创建自定义仪表盘示例")
        print("4. 列出现有表单和仪表盘")
        print("5. 退出")
        
        choice = input("\n请输入选项 (1-5): ").strip()
        
        if choice == "1":
            create_complete_volunteer_system()
        elif choice == "2":
            create_custom_form_example()
        elif choice == "3":
            create_custom_dashboard_example()
        elif choice == "4":
            list_existing_forms_and_dashboards()
        elif choice == "5":
            print("👋 再见！")
            break
        else:
            print("❌ 无效选项，请重新选择")