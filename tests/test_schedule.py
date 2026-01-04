"""
排班签到模型单元测试
测试ScheduleModel的所有功能
"""
import pytest
import sys
import os
import pandas as pd
from unittest.mock import Mock, patch
from datetime import datetime

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.schedule import ScheduleModel

class TestScheduleModel:
    """测试ScheduleModel类"""
    
    def setup_method(self):
        """每个测试方法前的设置"""
        self.mock_client = Mock()
        self.sample_schedule_data = {
            "义工姓名": "张三",
            "义工电话": "13800138000",
            "活动名称": "春节祈福法会",
            "活动日期": "2024-02-10",
            "开始时间": "09:00",
            "结束时间": "17:00",
            "活动地点": "大雄宝殿",
            "担任角色": "接待员",
            "签到状态": "已排班",
            "签到时间": None,
            "签退时间": None,
            "实际工时": 0,
            "备注": "请提前30分钟到场",
            "排班日期": "2024-02-05",
            "联系人": "李师兄"
        }
    
    @patch('models.schedule.JDYClient')
    def test_create_form_success(self, mock_jdy_client):
        """测试成功创建排班签到表单"""
        mock_instance = Mock()
        mock_instance.create_form.return_value = "form_schedule_123"
        mock_jdy_client.return_value = mock_instance
        
        result = ScheduleModel.create_form()
        
        assert result == "form_schedule_123"
        mock_instance.create_form.assert_called_once()
    
    @patch('models.schedule.JDYClient')
    def test_create_schedule_success(self, mock_jdy_client):
        """测试成功创建排班记录"""
        mock_instance = Mock()
        mock_instance.add_record.return_value = {"_id": "schedule_123", "status": "success"}
        mock_jdy_client.return_value = mock_instance
        
        result = ScheduleModel.create(**self.sample_schedule_data)
        
        assert result["status"] == "success"
        mock_instance.add_record.assert_called_once_with("排班签到", self.sample_schedule_data)
    
    @patch('models.schedule.JDYClient')
    def test_get_by_id_success(self, mock_jdy_client):
        """测试根据ID获取排班记录"""
        mock_instance = Mock()
        mock_instance.get_record.return_value = self.sample_schedule_data
        mock_jdy_client.return_value = mock_instance
        
        result = ScheduleModel.get_by_id("schedule_123")
        
        assert result == self.sample_schedule_data
        mock_instance.get_record.assert_called_once_with("排班签到", "schedule_123")
    
    @patch('models.schedule.JDYClient')
    def test_update_schedule_success(self, mock_jdy_client):
        """测试成功更新排班记录"""
        mock_instance = Mock()
        mock_instance.update_record.return_value = {"_id": "schedule_123", "status": "updated"}
        mock_jdy_client.return_value = mock_instance
        
        update_data = {"签到状态": "已确认", "实际工时": 8}
        result = ScheduleModel.update("schedule_123", **update_data)
        
        assert result["status"] == "updated"
        mock_instance.update_record.assert_called_once_with("排班签到", "schedule_123", update_data)
    
    @patch('models.schedule.JDYClient')
    def test_delete_schedule_success(self, mock_jdy_client):
        """测试成功删除排班记录"""
        mock_instance = Mock()
        mock_instance.delete_record.return_value = True
        mock_jdy_client.return_value = mock_instance
        
        result = ScheduleModel.delete("schedule_123")
        
        assert result is True
        mock_instance.delete_record.assert_called_once_with("排班签到", "schedule_123")
    
    @patch('models.schedule.JDYClient')
    def test_list_all_schedules(self, mock_jdy_client):
        """测试获取所有排班记录"""
        mock_instance = Mock()
        mock_data = [
            self.sample_schedule_data,
            {
                "义工姓名": "李四",
                "活动名称": "清明祭祖",
                "活动日期": "2024-04-04",
                "签到状态": "已确认"
            }
        ]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = ScheduleModel.list_all()
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 2
        assert result.iloc[0]["义工姓名"] == "张三"
        assert result.iloc[1]["义工姓名"] == "李四"
    
    @patch('models.schedule.JDYClient')
    def test_list_by_volunteer(self, mock_jdy_client):
        """测试获取指定义工的排班记录"""
        mock_instance = Mock()
        mock_data = [self.sample_schedule_data]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = ScheduleModel.list_by_volunteer("张三")
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]["义工姓名"] == "张三"
        mock_instance.get_records.assert_called_once_with("排班签到", {"义工姓名": "张三"})
    
    @patch('models.schedule.JDYClient')
    def test_list_by_event(self, mock_jdy_client):
        """测试获取指定活动的排班记录"""
        mock_instance = Mock()
        mock_data = [self.sample_schedule_data]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = ScheduleModel.list_by_event("春节祈福法会")
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]["活动名称"] == "春节祈福法会"
        mock_instance.get_records.assert_called_once_with("排班签到", {"活动名称": "春节祈福法会"})
    
    @patch('models.schedule.JDYClient')
    def test_list_by_date(self, mock_jdy_client):
        """测试获取指定日期的排班记录"""
        mock_instance = Mock()
        mock_data = [self.sample_schedule_data]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = ScheduleModel.list_by_date("2024-02-10")
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]["活动日期"] == "2024-02-10"
        mock_instance.get_records.assert_called_once_with("排班签到", {"活动日期": "2024-02-10"})
    
    @patch('models.schedule.JDYClient')
    def test_list_by_status(self, mock_jdy_client):
        """测试按签到状态筛选"""
        mock_instance = Mock()
        mock_data = [self.sample_schedule_data]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = ScheduleModel.list_by_status("已排班")
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        mock_instance.get_records.assert_called_once_with("排班签到", {"签到状态": "已排班"})
    
    @patch('models.schedule.JDYClient')
    def test_list_upcoming_schedules(self, mock_jdy_client):
        """测试获取即将进行的排班"""
        mock_instance = Mock()
        mock_data = [self.sample_schedule_data]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = ScheduleModel.list_upcoming_schedules()
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        mock_instance.get_records.assert_called_once()
    
    @patch('models.schedule.JDYClient')
    def test_check_in_success(self, mock_jdy_client):
        """测试义工签到成功"""
        mock_instance = Mock()
        mock_instance.update_record.return_value = {"_id": "schedule_123", "status": "checked_in"}
        mock_jdy_client.return_value = mock_instance
        
        with patch('models.schedule.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2024-02-10 08:30:00"
            result = ScheduleModel.check_in("schedule_123")
            
            assert result["status"] == "checked_in"
            mock_instance.update_record.assert_called_once_with(
                "排班签到", 
                "schedule_123", 
                {"签到状态": "已签到", "签到时间": "2024-02-10 08:30:00"}
            )
    
    @patch('models.schedule.JDYClient')
    def test_check_out_success(self, mock_jdy_client):
        """测试义工签退成功"""
        mock_instance = Mock()
        mock_instance.update_record.return_value = {"_id": "schedule_123", "status": "checked_out"}
        mock_jdy_client.return_value = mock_instance
        
        with patch('models.schedule.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2024-02-10 17:30:00"
            result = ScheduleModel.check_out("schedule_123", 8.0)
            
            assert result["status"] == "checked_out"
            mock_instance.update_record.assert_called_once_with(
                "排班签到", 
                "schedule_123", 
                {
                    "签到状态": "已签退", 
                    "签退时间": "2024-02-10 17:30:00",
                    "实际工时": 8.0
                }
            )
    
    @patch('models.schedule.JDYClient')
    def test_check_out_without_hours(self, mock_jdy_client):
        """测试义工签退（不指定工时）"""
        mock_instance = Mock()
        mock_instance.update_record.return_value = {"_id": "schedule_123", "status": "checked_out"}
        mock_instance.get_record.return_value = {"签到时间": "2024-02-10 08:30:00"}
        mock_jdy_client.return_value = mock_instance
        
        with patch('models.schedule.datetime') as mock_datetime:
            mock_datetime.now.return_value.strftime.return_value = "2024-02-10 17:30:00"
            result = ScheduleModel.check_out("schedule_123")
            
            assert result["status"] == "checked_out"
            mock_instance.update_record.assert_called_once_with(
                "排班签到", 
                "schedule_123", 
                {
                    "签到状态": "已签退", 
                    "签退时间": "2024-02-10 17:30:00",
                    "实际工时": 2.0
                }
            )
    
    @patch('models.schedule.JDYClient')
    def test_get_volunteer_hours(self, mock_jdy_client):
        """测试获取义工累计工时"""
        mock_instance = Mock()
        mock_data = [
            {"义工姓名": "张三", "实际工时": 8.0},
            {"义工姓名": "张三", "实际工时": 4.0}
        ]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = ScheduleModel.get_volunteer_hours("张三")
        
        assert result == 12.0
        mock_instance.get_records.assert_called_once_with("排班签到", {"义工姓名": "张三"})
    
    @patch('models.schedule.JDYClient')
    def test_get_volunteer_hours_empty(self, mock_jdy_client):
        """测试获取义工累计工时（无记录）"""
        mock_instance = Mock()
        mock_instance.get_records.return_value = []
        mock_jdy_client.return_value = mock_instance
        
        result = ScheduleModel.get_volunteer_hours("张三")
        
        assert result == 0.0
    
    @patch('models.schedule.JDYClient')
    def test_get_event_volunteers(self, mock_jdy_client):
        """测试获取活动的所有义工"""
        mock_instance = Mock()
        mock_data = [self.sample_schedule_data]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = ScheduleModel.get_event_volunteers("春节祈福法会")
        
        assert isinstance(result, pd.DataFrame)
        assert len(result) == 1
        assert result.iloc[0]["活动名称"] == "春节祈福法会"
    
    @patch('models.schedule.JDYClient')
    def test_get_schedule_count(self, mock_jdy_client):
        """测试获取排班记录总数"""
        mock_instance = Mock()
        mock_instance.get_record_count.return_value = 50
        mock_jdy_client.return_value = mock_instance
        
        result = ScheduleModel.get_schedule_count()
        
        assert result == 50
        mock_instance.get_record_count.assert_called_once_with("排班签到")
    
    @patch('models.schedule.JDYClient')
    def test_get_volunteer_schedule_count(self, mock_jdy_client):
        """测试获取义工参与次数"""
        mock_instance = Mock()
        mock_data = [
            {"义工姓名": "张三", "活动名称": "春节祈福法会"},
            {"义工姓名": "张三", "活动名称": "清明祭祖"}
        ]
        mock_instance.get_records.return_value = mock_data
        mock_jdy_client.return_value = mock_instance
        
        result = ScheduleModel.get_volunteer_schedule_count("张三")
        
        assert result == 2
        mock_instance.get_records.assert_called_once_with("排班签到", {"义工姓名": "张三"})
    
    def test_field_constants(self):
        """测试字段常量定义"""
        assert ScheduleModel.FORM_NAME == "排班签到"
        assert ScheduleModel.FIELD_VOLUNTEER_NAME == "义工姓名"
        assert ScheduleModel.FIELD_VOLUNTEER_PHONE == "义工电话"
        assert ScheduleModel.FIELD_EVENT_NAME == "活动名称"
        assert ScheduleModel.FIELD_EVENT_DATE == "活动日期"
        assert ScheduleModel.FIELD_START_TIME == "开始时间"
        assert ScheduleModel.FIELD_END_TIME == "结束时间"
        assert ScheduleModel.FIELD_LOCATION == "活动地点"
        assert ScheduleModel.FIELD_ROLE == "担任角色"
        assert ScheduleModel.FIELD_STATUS == "签到状态"
        assert ScheduleModel.FIELD_ACTUAL_HOURS == "实际工时"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])