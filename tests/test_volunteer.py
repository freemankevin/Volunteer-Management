"""
义工档案模型单元测试
测试VolunteerModel的所有功能
"""
import pytest
import sys
import os
import pandas as pd
from unittest.mock import Mock, patch

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.volunteer import VolunteerModel

class TestVolunteerModel:
    """测试VolunteerModel类"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.mock_client = Mock()
        self.sample_volunteer_data = {
            "姓名": "张三",
            "手机号": "13800138000",
            "邮箱": "zhangsan@example.com",
            "年龄": 35,
            "性别": "男",
            "住址": "广州市越秀区",
            "紧急联系人": "张父",
            "紧急联系电话": "13900139000",
            "技能特长": "医疗、摄影",
            "义工经验": "5年医院义工经验",
            "可服务时间": ["周末白天", "工作日晚上"],
            "义工类型": ["医疗义工", "摄影义工"],
            "加入日期": "2024-01-15",
            "状态": "活跃",
            "累计工时": 120,
            "备注": "热心义工，技能全面"
        }
    
    @patch('models.volunteer.JDYClient')
    def test_create_form_success(self, mock_jdy_client):
        """测试成功创建义工档案表单"""
        mock_instance = Mock()
        mock_instance.create_form.return_value = "form_123456"
        mock_jdy_client.return_value = mock_instance
        
        result = VolunteerModel.create_form()
        
        assert result == "form_123456"
        mock_instance.create_form.assert_called_once()
    
    @patch('models.volunteer.JDYClient')
    def test_create_volunteer_success(self, mock_jdy_client):
        """测试成功创建义工记录"""
        mock_instance = Mock()
        mock_instance.add_record.return_value = {"_id": "record_123", "status": "success"}
        mock_jdy_client.return_value = mock_instance
        
        result = VolunteerModel.create(**self.sample_volunteer_data)
        
        assert result["status"] == "success"
        mock_instance.add_record.assert_called_once_with("义工档案", self.sample_volunteer_data)
    
    @patch('models.volunteer.JDYClient')
    def test_get_by_id_success(self, mock_jdy_client):
        """测试根据ID获取义工信息"""
        mock_instance = Mock()
        mock_instance.get_record.return_value = self.sample_volunteer_data
        mock_jdy_client.return_value = mock_instance
        
        result = VolunteerModel.get_by_id("record_123")
        
        assert result == self.sample_volunteer_data
        mock_instance.get_record.assert_called_once_with("义工档案", "record_123")
    
    @patch('models.volunteer.JDYClient')
    def test_update_volunteer_success(self, mock_jdy_client):
        """测试成功更新义工信息"""
        mock_instance = Mock()
        mock_instance.update_record.return_value = {"_id": "record_123", "status": "updated"}
        mock_jdy_client.return_value = mock_instance
        
        update_data = {"累计工时": 150, "状态": "活跃"}
        result = VolunteerModel.update("record_123", **update_data)
        
        assert result["status"] == "updated"
        mock_instance.update_record.assert_called_once_with("义工档案", "record_123", update_data)
    
    @patch('models.volunteer.JDYClient')
    def test_delete_volunteer_success(self, mock_jdy_client):
        """测试成功删除义工记录"""
        mock_instance = Mock()
        mock_instance.delete_record.return_value = True
        mock_jdy_client.return_value = mock_instance
        
        result = VolunteerModel.delete("record_123")
        
        assert result is True
        mock_instance.delete_record.assert_called_once_with("义工档案", "record_123")
    
    @patch('models.volunteer.JDYClient')
    def test_list_all_volunteers(self, mock_jdy_client):
        """测试获取所有义工列表"""
        mock_instance = Mock()
        mock_data = [
            self.sample_volunteer_data,
            {
                "姓名": "李四",
                "手机号": "13900139000",
                "年龄": 28,
                "状态": "活跃"
            }
        ]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = VolunteerModel.list_all()
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert result.iloc[0]["姓名"] == "张三"
        assert result.iloc[1]["姓名"] == "李四"
    
    @patch('models.volunteer.JDYClient')
    def test_list_by_skill(self, mock_jdy_client):
        """测试按技能筛选义工"""
        mock_instance = Mock()
        mock_data = [self.sample_volunteer_data]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = VolunteerModel.list_by_skill("医疗")
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        mock_instance.get_records.assert_called_once_with("义工档案", {"技能特长": "医疗"})
    
    @patch('models.volunteer.JDYClient')
    def test_list_by_status(self, mock_jdy_client):
        """测试按状态筛选义工"""
        mock_instance = Mock()
        mock_data = [self.sample_volunteer_data]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = VolunteerModel.list_by_status("活跃")
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        mock_instance.get_records.assert_called_once_with("义工档案", {"状态": "活跃"})
    
    @patch('models.volunteer.JDYClient')
    def test_list_by_volunteer_type(self, mock_jdy_client):
        """测试按义工类型筛选"""
        mock_instance = Mock()
        mock_data = [self.sample_volunteer_data]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = VolunteerModel.list_by_volunteer_type("医疗义工")
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        mock_instance.get_records.assert_called_once_with("义工档案", {"义工类型": "医疗义工"})
    
    @patch('models.volunteer.JDYClient')
    def test_search_by_name(self, mock_jdy_client):
        """测试按姓名搜索义工"""
        mock_instance = Mock()
        mock_data = [self.sample_volunteer_data]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = VolunteerModel.search_by_name("张三")
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]["姓名"] == "张三"
        mock_instance.get_records.assert_called_once_with("义工档案", {"姓名": "张三"})
    
    @patch('models.volunteer.JDYClient')
    def test_get_volunteer_count(self, mock_jdy_client):
        """测试获取义工总数"""
        mock_instance = Mock()
        mock_instance.get_record_count.return_value = 25
        mock_jdy_client.return_value = mock_instance
        
        result = VolunteerModel.get_volunteer_count()
        
        assert result == 25
        mock_instance.get_record_count.assert_called_once_with("义工档案")
    
    @patch('models.volunteer.JDYClient')
    def test_get_active_volunteers(self, mock_jdy_client):
        """测试获取活跃义工列表"""
        mock_instance = Mock()
        mock_data = [self.sample_volunteer_data]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = VolunteerModel.get_active_volunteers()
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]["状态"] == "活跃"
    
    def test_field_constants(self):
        """测试字段常量定义"""
        assert VolunteerModel.FORM_NAME == "义工档案"
        assert VolunteerModel.FIELD_NAME == "姓名"
        assert VolunteerModel.FIELD_PHONE == "手机号"
        assert VolunteerModel.FIELD_EMAIL == "邮箱"
        assert VolunteerModel.FIELD_AGE == "年龄"
        assert VolunteerModel.FIELD_GENDER == "性别"
        assert VolunteerModel.FIELD_STATUS == "状态"
        assert VolunteerModel.FIELD_TOTAL_HOURS == "累计工时"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])