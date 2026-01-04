from core.api_client import JDYClient
from config.settings import SCHEDULE_ENTRY_ID
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime

class ScheduleModel:
    FORM_NAME = "排班签到"
    ENTRY_ID = SCHEDULE_ENTRY_ID
    
    FIELD_VOLUNTEER_NAME = "义工姓名"
    FIELD_VOLUNTEER_PHONE = "义工电话"
    FIELD_EVENT_NAME = "活动名称"
    FIELD_EVENT_DATE = "活动日期"
    FIELD_START_TIME = "开始时间"
    FIELD_END_TIME = "结束时间"
    FIELD_LOCATION = "活动地点"
    FIELD_ROLE = "担任角色"
    FIELD_STATUS = "签到状态"
    FIELD_CHECK_IN_TIME = "签到时间"
    FIELD_CHECK_OUT_TIME = "签退时间"
    FIELD_ACTUAL_HOURS = "实际工时"
    FIELD_REMARKS = "备注"
    FIELD_SCHEDULE_DATE = "排班日期"
    FIELD_CONTACT_PERSON = "联系人"
    
    @classmethod
    def create(cls, **data) -> str:
        """创建排班记录"""
        client = JDYClient()
        return client.create_data(cls.ENTRY_ID, data)
    
    @classmethod
    def get_by_id(cls, record_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取排班记录"""
        client = JDYClient()
        return client.get_data(cls.ENTRY_ID, record_id)
    
    @classmethod
    def update(cls, record_id: str, **data) -> bool:
        """更新排班记录"""
        client = JDYClient()
        return client.update_data(cls.ENTRY_ID, record_id, data)
    
    @classmethod
    def delete(cls, record_id: str) -> bool:
        """删除排班记录"""
        client = JDYClient()
        return client.delete_data(cls.ENTRY_ID, record_id)
    
    @classmethod
    def list_all(cls) -> pd.DataFrame:
        """获取所有排班记录"""
        client = JDYClient()
        data = client.query_data(cls.ENTRY_ID)
        return pd.DataFrame(data)
    
    @classmethod
    def list_by_volunteer(cls, volunteer_name: str) -> pd.DataFrame:
        """获取指定义工的排班记录"""
        client = JDYClient()
        filters = {
            "rel": "and",
            "cond": [{
                "field": cls.FIELD_VOLUNTEER_NAME,
                "type": "text",
                "method": "eq",
                "value": [volunteer_name]
            }]
        }
        data = client.query_data(cls.ENTRY_ID, filters=filters)
        return pd.DataFrame(data)
    
    @classmethod
    def list_by_event(cls, event_name: str) -> pd.DataFrame:
        """获取指定活动的排班记录"""
        client = JDYClient()
        filters = {
            "rel": "and",
            "cond": [{
                "field": cls.FIELD_EVENT_NAME,
                "type": "text",
                "method": "eq",
                "value": [event_name]
            }]
        }
        data = client.query_data(cls.ENTRY_ID, filters=filters)
        return pd.DataFrame(data)
    
    @classmethod
    def list_by_status(cls, status: str) -> pd.DataFrame:
        """按签到状态筛选"""
        client = JDYClient()
        filters = {
            "rel": "and",
            "cond": [{
                "field": cls.FIELD_STATUS,
                "type": "text",
                "method": "eq",
                "value": [status]
            }]
        }
        data = client.query_data(cls.ENTRY_ID, filters=filters)
        return pd.DataFrame(data)
    
    @classmethod
    def check_in(cls, record_id: str) -> bool:
        """义工签到"""
        check_in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return cls.update(record_id, **{
            cls.FIELD_STATUS: "已签到",
            cls.FIELD_CHECK_IN_TIME: check_in_time
        })
    
    @classmethod
    def check_out(cls, record_id: str, actual_hours: float = None) -> bool:
        """义工签退"""
        check_out_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_data = {
            cls.FIELD_STATUS: "已签退",
            cls.FIELD_CHECK_OUT_TIME: check_out_time
        }
        
        if actual_hours is not None:
            update_data[cls.FIELD_ACTUAL_HOURS] = actual_hours
        
        return cls.update(record_id, **update_data)
    
    @classmethod
    def get_volunteer_hours(cls, volunteer_name: str) -> float:
        """获取义工累计工时"""
        schedules = cls.list_by_volunteer(volunteer_name)
        if schedules.empty:
            return 0.0
        
        total_hours = schedules[cls.FIELD_ACTUAL_HOURS].sum()
        return float(total_hours)
    
    @classmethod
    def get_event_volunteers(cls, event_name: str) -> pd.DataFrame:
        """获取活动的所有义工"""
        return cls.list_by_event(event_name)
    
    @classmethod
    def get_schedule_count(cls) -> int:
        """获取排班记录总数"""
        data = cls.list_all()
        return len(data)