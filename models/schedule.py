from core.api_client import JDYClient
from config.settings import SCHEDULE_ENTRY_ID
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime

class ScheduleModel:
    FORM_NAME = "排班签到"
    ENTRY_ID = SCHEDULE_ENTRY_ID
    
    # 字段映射到 widget ID
    FIELD_NAME = "_widget_1767577273272"               # 姓名
    FIELD_PHONE = "_widget_1767577273274"              # 手机号
    FIELD_GENDER = "_widget_1767577273275"             # 性别
    FIELD_EVENT_NAME = "_widget_1767577507155"         # 活动名称
    FIELD_EVENT_DATE = "_widget_1767577507156"         # 活动日期
    FIELD_EVENT_TIME = "_widget_1767577507158"         # 活动时间
    FIELD_LOCATION = "_widget_1767577507159"           # 活动地点
    FIELD_ROLE = "_widget_1767577975108"               # 担任角色
    FIELD_STATUS = "_widget_1767577975110"             # 排班状态
    FIELD_CHECK_IN_TIME = "_widget_1767577975112"      # 签到时间
    FIELD_CHECK_OUT_TIME = "_widget_1767577975113"     # 签退时间
    FIELD_ACTUAL_HOURS = "_widget_1767577975114"       # 实际工时
    FIELD_WORK_PERFORMANCE = "_widget_1767577975115"   # 工作表现
    FIELD_REMARKS = "_widget_1767577975117"            # 备注
    
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
    def list_by_volunteer(cls, name: str) -> pd.DataFrame:
        """获取指定义工的排班记录"""
        client = JDYClient()
        filters = {
            "rel": "and",
            "cond": [{
                "field": cls.FIELD_NAME,
                "type": "text",
                "method": "eq",
                "value": [name]
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
        """按排班状态筛选"""
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
    def get_volunteer_hours(cls, name: str) -> float:
        """获取义工累计工时"""
        schedules = cls.list_by_volunteer(name)
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