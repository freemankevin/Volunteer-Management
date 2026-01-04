"""
寺院义工管理系统创建示例
专为寺院义工招募、管理、活动报名等场景设计
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.form_builder import TempleVolunteerFormBuilder
from services.dashboard_builder import TempleVolunteerDashboardBuilder
from core.api_client import JDYClient
import logging

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_complete_temple_volunteer_system():
    """创建完整的寺院义工管理系统"""
    
    print("🙏 开始创建寺院义工管理系统...")
    
    # 初始化构建器
    form_builder = TempleVolunteerFormBuilder()
    dashboard_builder = TempleVolunteerDashboardBuilder()
    
    try:
        # 1. 创建寺院专用表单
        print("📋 创建寺院专用表单...")
        
        # 创建寺院义工注册表单
        volunteer_form = form_builder.create_temple_volunteer_registration_form()
        print(f"✅ 寺院义工注册表单创建成功: {volunteer_form}")
        
        # 创建寺院活动报名表单
        activity_form = form_builder.create_temple_activity_registration_form()
        print(f"✅ 寺院活动报名表单创建成功: {activity_form}")
        
        # 创建寺院活动反馈表单
        feedback_form = form_builder.create_temple_feedback_form()
        print(f"✅ 寺院活动反馈表单创建成功: {feedback_form}")
        
        # 2. 创建寺院专用仪表盘
        print("📊 创建寺院专用仪表盘...")
        
        # 创建寺院义工管理仪表盘
        volunteer_dashboard = dashboard_builder.create_temple_volunteer_dashboard(
            volunteer_form, activity_form, feedback_form
        )
        print(f"✅ 寺院义工管理仪表盘创建成功: {volunteer_dashboard}")
        
        # 创建寺院法务活动管理仪表盘
        activity_dashboard = dashboard_builder.create_temple_activity_dashboard(
            activity_form, feedback_form
        )
        print(f"✅ 寺院法务活动管理仪表盘创建成功: {activity_dashboard}")
        
        # 创建寺院义工综合分析仪表盘
        analysis_dashboard = dashboard_builder.create_temple_volunteer_analysis_dashboard(
            volunteer_form, activity_form
        )
        print(f"✅ 寺院义工综合分析仪表盘创建成功: {analysis_dashboard}")
        
        # 3. 输出完整系统信息
        print("\n🎉 寺院义工管理系统创建完成！")
        print("=" * 60)
        print("📋 寺院专用表单:")
        print(f"  寺院义工注册表单: {volunteer_form}")
        print(f"  寺院活动报名表单: {activity_form}")
        print(f"  寺院活动反馈表单: {feedback_form}")
        print("\n📊 寺院专用仪表盘:")
        print(f"  寺院义工管理仪表盘: {volunteer_dashboard}")
        print(f"  寺院法务活动管理仪表盘: {activity_dashboard}")
        print(f"  寺院义工综合分析仪表盘: {analysis_dashboard}")
        print("=" * 60)
        
        # 4. 生成使用指南
        print("\n📖 使用指南:")
        print("1. 寺院义工注册表单 - 用于义工招募和信息登记")
        print("2. 寺院活动报名表单 - 用于法会、讲座等活动报名")
        print("3. 寺院活动反馈表单 - 用于收集活动反馈和改进建议")
        print("4. 寺院义工管理仪表盘 - 总览义工数据和活动统计")
        print("5. 寺院法务活动管理仪表盘 - 专门管理法务活动数据")
        print("6. 寺院义工综合分析仪表盘 - 深度分析义工参与度和活动效果")
        
        return {
            "forms": {
                "temple_volunteer_registration": volunteer_form,
                "temple_activity_registration": activity_form,
                "temple_activity_feedback": feedback_form
            },
            "dashboards": {
                "temple_volunteer_management": volunteer_dashboard,
                "temple_activity_management": activity_dashboard,
                "temple_volunteer_analysis": analysis_dashboard
            }
        }
        
    except Exception as e:
        logger.error(f"创建寺院义工管理系统时出错: {str(e)}")
        raise

def create_temple_volunteer_registration_demo():
    """创建寺院义工注册演示"""
    print("\n📝 创建寺院义工注册演示...")
    
    form_builder = TempleVolunteerFormBuilder()
    
    # 创建自定义寺院义工注册表单
    custom_form = (form_builder
                  .add_text_field("dharma_name", "法名")
                  .add_select_field("precepts", "受戒情况", ["未受戒", "五戒", "菩萨戒", "出家戒"])
                  .add_textarea_field("practice_experience", "修行经历")
                  .add_select_field("preferred_service", "偏好服务", [
                      "殿堂护持", "香客接待", "素食制作", "环境清洁", 
                      "花木养护", "法物流通", "摄影记录", "医疗协助"
                  ], multiple=True)
                  .create_custom_form("寺院义工详细登记表", "寺院义工详细信息和偏好登记"))
    
    print(f"✅ 自定义寺院义工表单创建成功: {custom_form}")
    return custom_form

def create_temple_activity_demo():
    """创建寺院活动演示"""
    print("\n🪷 创建寺院活动演示...")
    
    form_builder = TempleVolunteerFormBuilder()
    
    # 创建特定法会活动报名
    water_liberation_form = (form_builder
                           .add_text_field("activity_name", "活动名称", required=True)
                           .add_date_field("activity_date", "活动日期", required=True)
                           .add_select_field("activity_type", "法会类型", [
                               "盂兰盆法会", "水陆法会", "瑜伽焰口", "斋天法会",
                               "供佛斋僧", "放生法会", "诵经法会", "禅修活动"
                           ], required=True)
                           .add_number_field("merit_dedication", "功德回向人数", min_value=1)
                           .add_textarea_field("dedication_content", "回向内容")
                           .create_custom_form("法会活动报名", "寺院法会活动报名和功德回向"))
    
    print(f"✅ 法会活动报名表单创建成功: {water_liberation_form}")
    return water_liberation_form

def show_usage_examples():
    """显示使用示例"""
    print("\n📖 寺院义工管理系统使用示例:")
    print("=" * 50)
    
    examples = [
        {
            "场景": "义工招募",
            "表单": "寺院义工注册表单",
            "用途": "收集义工基本信息、联系方式、服务偏好"
        },
        {
            "场景": "法会报名",
            "表单": "寺院活动报名表单",
            "用途": "盂兰盆法会、水陆法会等活动报名"
        },
        {
            "场景": "活动反馈",
            "表单": "寺院活动反馈表单",
            "用途": "收集参与者反馈，改进法务活动"
        },
        {
            "场景": "数据总览",
            "仪表盘": "寺院义工管理仪表盘",
            "用途": "总览义工人数、活动统计、满意度"
        },
        {
            "场景": "活动管理",
            "仪表盘": "寺院法务活动管理",
            "用途": "管理法会活动数据、报名统计"
        },
        {
            "场景": "深度分析",
            "仪表盘": "寺院义工综合分析",
            "用途": "分析义工参与度、活动效果、时间分布"
        }
    ]
    
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example['场景']}")
        print(f"   {list(example.keys())[1]}: {example[list(example.keys())[1]]}")
        print(f"   用途: {example['用途']}")
        print()

if __name__ == "__main__":
    print("🏯 寺院义工管理系统")
    print("=" * 50)
    
    while True:
        print("\n请选择操作:")
        print("1. 创建完整的寺院义工管理系统")
        print("2. 创建寺院义工注册演示")
        print("3. 创建寺院活动演示")
        print("4. 显示使用示例")
        print("5. 退出")
        
        choice = input("\n请输入选项 (1-5): ").strip()
        
        if choice == "1":
            create_complete_temple_volunteer_system()
        elif choice == "2":
            create_temple_volunteer_registration_demo()
        elif choice == "3":
            create_temple_activity_demo()
        elif choice == "4":
            show_usage_examples()
        elif choice == "5":
            print("🙏 阿弥陀佛！")
            break
        else:
            print("❌ 无效选项，请重新选择")