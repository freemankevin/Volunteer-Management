"""
活动库模型单元测试
测试EventModel的所有功能
"""
import pytest
import sys
import os
import pandas as pd
from unittest.mock import Mock, patch
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.event import EventModel

class TestEventModel:
    """测试EventModel类"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.mock_client = Mock()
        self.sample_event_data = {
            "活动名称": "春节祈福法会",
            "活动类型": "法会活动",
            "活动日期": "2024-02-10",
            "开始时间": "09:00",
            "结束时间": "17:00",
            "活动地点": "大雄宝殿",
            "活动描述": "春节祈福法会，欢迎信众参加",
            "需要义工人数": 10,
            "所需技能": ["接待经验", "文书处理"],
            "联系人": "李师兄",
            "联系电话": "13700137000",
            "活动状态": "报名中",
            "报名截止日": "2024-02-08",
            "最大参与人数": 50,
            "当前参与人数": 25,
            "备注": "请义工提前30分钟到场"
        }
    
    @patch('models.event.JDYClient')
    def test_create_form_success(self, mock_jdy_client):
        """测试成功创建活动库表单"""
        mock_instance = Mock()
        mock_instance.create_form.return_value = "form_event_123"
        mock_jdy_client.return_value = mock_instance
        
        result = EventModel.create_form()
        
        assert result == "form_event_123"
        mock_instance.create_form.assert_called_once()
    
    @patch('models.event.JDYClient')
    def test_create_event_success(self, mock_jdy_client):
        """测试成功创建活动记录"""
        mock_instance = Mock()
        mock_instance.add_record.return_value = {"_id": "event_123", "status": "success"}
        mock_jdy_client.return_value = mock_instance
        
        result = EventModel.create(**self.sample_event_data)
        
        assert result["status"] == "success"
        mock_instance.add_record.assert_called_once_with("活动库", self.sample_event_data)
    
    @patch('models.event.JDYClient')
    def test_get_by_id_success(self, mock_jdy_client):
        """测试根据ID获取活动信息"""
        mock_instance = Mock()
        mock_instance.get_record.return_value = self.sample_event_data
        mock_jdy_client.return_value = mock_instance
        
        result = EventModel.get_by_id("event_123")
        
        assert result == self.sample_event_data
        mock_instance.get_record.assert_called_once_with("活动库", "event_123")
    
    @patch('models.event.JDYClient')
    def test_update_event_success(self, mock_jdy_client):
        """测试成功更新活动信息"""
        mock_instance = Mock()
        mock_instance.update_record.return_value = {"_id": "event_123", "status": "updated"}
        mock_jdy_client.return_value = mock_instance
        
        update_data = {"当前参与人数": 30, "活动状态": "进行中"}
        result = EventModel.update("event_123", **update_data)
        
        assert result["status"] == "updated"
        mock_instance.update_record.assert_called_once_with("活动库", "event_123", update_data)
    
    @patch('models.event.JDYClient')
    def test_delete_event_success(self, mock_jdy_client):
        """测试成功删除活动记录"""
        mock_instance = Mock()
        mock_instance.delete_record.return_value = True
        mock_jdy_client.return_value = mock_instance
        
        result = EventModel.delete("event_123")
        
        assert result is True
        mock_instance.delete_record.assert_called_once_with("活动库", "event_123")
    
    @patch('models.event.JDYClient')
    def test_list_all_events(self, mock_jdy_client):
        """测试获取所有活动列表"""
        mock_instance = Mock()
        mock_data = [
            self.sample_event_data,
            {
                "活动名称": "清明祭祖",
                "活动类型": "法会活动",
                "活动日期": "2024-04-04",
                "活动状态": "计划中"
            }
        ]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = EventModel.list_all()
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert result.iloc[0]["活动名称"] == "春节祈福法会"
        assert result.iloc[1]["活动名称"] == "清明祭祖"
    
    @patch('models.event.JDYClient')
    def test_list_by_type(self, mock_jdy_client):
        """测试按活动类型筛选"""
        mock_instance = Mock()
        mock_data = [self.sample_event_data]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = EventModel.list_by_type("法会活动")
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        mock_instance.get_records.assert_called_once_with("活动库", {"活动类型": "法会活动"})
    
    @patch('models.event.JDYClient')
    def test_list_by_status(self, mock_jdy_client):
        """测试按活动状态筛选"""
        mock_instance = Mock()
        mock_data = [self.sample_event_data]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = EventModel.list_by_status("报名中")
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        mock_instance.get_records.assert_called_once_with("活动库", {"活动状态": "报名中"})
    
    @patch('models.event.JDYClient')
    def test_list_upcoming_events(self, mock_jdy_client):
        """测试获取即将进行的活动"""
        mock_instance = Mock()
        mock_data = [self.sample_event_data]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = EventModel.list_upcoming_events()
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        mock_instance.get_records.assert_called_once()
    
    @patch('models.event.JDYClient')
    def test_search_by_name(self, mock_jdy_client):
        """测试按活动名称搜索"""
        mock_instance = Mock()
        mock_data = [self.sample_event_data]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = EventModel.search_by_name("春节祈福法会")
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]["活动名称"] == "春节祈福法会"
        mock_instance.get_records.assert_called_once_with("活动库", {"活动名称": "春节祈福法会"})
    
    @patch('models.event.JDYClient')
    def test_get_event_count(self, mock_jdy_client):
        """测试获取活动总数"""
        mock_instance = Mock()
        mock_instance.get_record_count.return_value = 15
        mock_jdy_client.return_value = mock_instance
        
        result = EventModel.get_event_count()
        
        assert result == 15
        mock_instance.get_record_count.assert_called_once_with("活动库")
    
    @patch('models.event.JDYClient')
    def test_get_events_by_date_range(self, mock_jdy_client):
        """测试获取指定日期范围内的活动"""
        mock_instance = Mock()
        mock_data = [self.sample_event_data]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = EventModel.get_events_by_date_range("2024-02-01", "2024-02-28")
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        mock_instance.get_records.assert_called_once()
    
    def test_field_constants(self):
        """测试字段常量定义"""
        assert EventModel.FORM_NAME == "活动库"
        assert EventModel.FIELD_EVENT_NAME == "活动名称"
        assert EventModel.FIELD_EVENT_TYPE == "活动类型"
        assert EventModel.FIELD_EVENT_DATE == "活动日期"
        assert EventModel.FIELD_START_TIME == "开始时间"
        assert EventModel.FIELD_END_TIME == "结束时间"
        assert EventModel.FIELD_LOCATION == "活动地点"
        assert EventModel.FIELD_STATUS == "活动状态"
        assert EventModel.FIELD_REQUIRED_VOLUNTEERS == "需要义工人数"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])