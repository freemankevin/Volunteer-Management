"""
简道云API集成测试
测试表单和仪表盘创建功能
"""
import pytest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from services.form_builder import TempleVolunteerFormBuilder
from services.dashboard_builder import TempleVolunteerDashboardBuilder
from core.api_client import JDYClient

class TestJDYIntegration:
    """简道云集成测试类"""
    
    def setup_method(self):
        """测试初始化"""
        self.form_builder = TempleVolunteerFormBuilder()
        self.dashboard_builder = TempleVolunteerDashboardBuilder()
        self.client = JDYClient()
    
    def test_api_connection(self):
        """测试API连接"""
        try:
            forms = self.client.get_form_list()
            assert isinstance(forms, list)
            print("✅ API连接测试通过")
        except Exception as e:
            pytest.fail(f"API连接失败: {str(e)}")
    
    def test_create_custom_form(self):
        """测试创建自定义表单"""
        try:
            form_id = (self.form_builder
                      .add_text_field("test_name", "测试名称", required=True)
                      .add_email_field("test_email", "测试邮箱")
                      .create_custom_form("测试表单", "这是一个测试表单"))
            
            assert form_id is not None
            assert len(form_id) > 0
            print(f"✅ 自定义表单创建测试通过: {form_id}")
            
            # 清理测试数据
            self.client.delete_form(form_id)
            print(f"🧹 测试表单已删除: {form_id}")
            
        except Exception as e:
            pytest.fail(f"创建自定义表单失败: {str(e)}")
    
    def test_create_temple_forms(self):
        """测试创建寺院义工表单"""
        try:
            # 测试寺院义工注册表单
            volunteer_form_id = self.form_builder.create_temple_volunteer_registration_form()
            assert volunteer_form_id is not None
            print(f"✅ 寺院义工注册表单创建测试通过: {volunteer_form_id}")
            
            # 测试寺院活动报名表单
            activity_form_id = self.form_builder.create_temple_activity_registration_form()
            assert activity_form_id is not None
            print(f"✅ 寺院活动报名表单创建测试通过: {activity_form_id}")
            
            # 测试寺院活动反馈表单
            feedback_form_id = self.form_builder.create_temple_feedback_form()
            assert feedback_form_id is not None
            print(f"✅ 寺院活动反馈表单创建测试通过: {feedback_form_id}")
            
            # 清理测试数据
            for form_id in [volunteer_form_id, activity_form_id, feedback_form_id]:
                try:
                    self.client.delete_form(form_id)
                    print(f"🧹 测试表单已删除: {form_id}")
                except:
                    pass  # 忽略删除错误
                    
        except Exception as e:
            pytest.fail(f"创建寺院义工表单失败: {str(e)}")
    
    def test_form_field_types(self):
        """测试各种表单字段类型"""
        try:
            form_id = (self.form_builder
                      .add_text_field("text_field", "文本字段", required=True)
                      .add_number_field("number_field", "数字字段", min_value=1, max_value=100)
                      .add_date_field("date_field", "日期字段")
                      .add_select_field("select_field", "选择字段", ["选项1", "选项2", "选项3"])
                      .add_textarea_field("textarea_field", "多行文本")
                      .add_phone_field("phone_field", "手机号")
                      .add_email_field("email_field", "邮箱")
                      .add_image_field("image_field", "图片上传")
                      .create_custom_form("字段类型测试", "测试所有字段类型"))
            
            assert form_id is not None
            print(f"✅ 字段类型测试通过: {form_id}")
            
            # 清理测试数据
            self.client.delete_form(form_id)
            print(f"🧹 测试表单已删除: {form_id}")
            
        except Exception as e:
            pytest.fail(f"字段类型测试失败: {str(e)}")
    
    def test_list_forms(self):
        """测试获取表单列表"""
        try:
            forms = self.client.get_form_list()
            assert isinstance(forms, list)
            print(f"✅ 获取表单列表测试通过，共 {len(forms)} 个表单")
        except Exception as e:
            pytest.fail(f"获取表单列表失败: {str(e)}")
    
    def test_list_dashboards(self):
        """测试获取仪表盘列表"""
        try:
            dashboards = self.client.get_dashboard_list()
            assert isinstance(dashboards, list)
            print(f"✅ 获取仪表盘列表测试通过，共 {len(dashboards)} 个仪表盘")
        except Exception as e:
            pytest.fail(f"获取仪表盘列表失败: {str(e)}")

def run_tests():
    """运行所有测试"""
    print("🧪 开始运行简道云集成测试...")
    
    test_instance = TestJDYIntegration()
    
    tests = [
        test_instance.test_api_connection,
        test_instance.test_list_forms,
        test_instance.test_list_dashboards,
        test_instance.test_create_custom_form,
        test_instance.test_form_field_types,
        test_instance.test_create_temple_forms
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test_instance.setup_method()
            test()
            passed += 1
        except Exception as e:
            print(f"❌ 测试失败: {test.__name__} - {str(e)}")
            failed += 1
    
    print(f"\n📊 测试结果:")
    print(f"  通过: {passed}")
    print(f"  失败: {failed}")
    print(f"  总计: {passed + failed}")
    
    if failed == 0:
        print("🎉 所有测试通过！")
    else:
        print(f"⚠️  {failed} 个测试失败")

if __name__ == "__main__":
    run_tests()