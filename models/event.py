from core.api_client import JDYClient
from config.settings import EVENT_ENTRY_ID
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime

class EventModel:
    FORM_NAME = "活动库"
    ENTRY_ID = EVENT_ENTRY_ID
    
    FIELD_EVENT_NAME = "活动名称"
    FIELD_EVENT_TYPE = "活动类型"
    FIELD_EVENT_DATE = "活动日期"
    FIELD_START_TIME = "开始时间"
    FIELD_END_TIME = "结束时间"
    FIELD_LOCATION = "活动地点"
    FIELD_DESCRIPTION = "活动描述"
    FIELD_REQUIRED_VOLUNTEERS = "需要义工人数"
    FIELD_REQUIRED_SKILLS = "所需技能"
    FIELD_CONTACT_PERSON = "联系人"
    FIELD_CONTACT_PHONE = "联系电话"
    FIELD_STATUS = "活动状态"
    FIELD_REGISTRATION_DEADLINE = "报名截止日"
    FIELD_MAX_PARTICIPANTS = "最大参与人数"
    FIELD_CURRENT_PARTICIPANTS = "当前参与人数"
    FIELD_NOTES = "备注"
    
    @classmethod
    def create(cls, **data) -> str:
        """创建新活动"""
        client = JDYClient()
        return client.create_data(cls.ENTRY_ID, data)
    
    @classmethod
    def get_by_id(cls, record_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取活动信息"""
        client = JDYClient()
        return client.get_data(cls.ENTRY_ID, record_id)
    
    @classmethod
    def update(cls, record_id: str, **data) -> bool:
        """更新活动信息"""
        client = JDYClient()
        return client.update_data(cls.ENTRY_ID, record_id, data)
    
    @classmethod
    def delete(cls, record_id: str) -> bool:
        """删除活动记录"""
        client = JDYClient()
        return client.delete_data(cls.ENTRY_ID, record_id)
    
    @classmethod
    def list_all(cls) -> pd.DataFrame:
        """获取所有活动列表"""
        client = JDYClient()
        data = client.query_data(cls.ENTRY_ID)
        return pd.DataFrame(data)
    
    @classmethod
    def list_by_type(cls, event_type: str) -> pd.DataFrame:
        """按活动类型筛选"""
        client = JDYClient()
        filters = {
            "rel": "and",
            "cond": [{
                "field": cls.FIELD_EVENT_TYPE,
                "type": "text",
                "method": "eq",
                "value": [event_type]
            }]
        }
        data = client.query_data(cls.ENTRY_ID, filters=filters)
        return pd.DataFrame(data)
    
    @classmethod
    def list_by_status(cls, status: str) -> pd.DataFrame:
        """按活动状态筛选"""
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
    def search_by_name(cls, name: str) -> pd.DataFrame:
        """按活动名称搜索"""
        client = JDYClient()
        filters = {
            "rel": "and",
            "cond": [{
                "field": cls.FIELD_EVENT_NAME,
                "type": "text",
                "method": "eq",
                "value": [name]
            }]
        }
        data = client.query_data(cls.ENTRY_ID, filters=filters)
        return pd.DataFrame(data)
    
    @classmethod
    def get_event_count(cls) -> int:
        """获取活动总数"""
        data = cls.list_all()
        return len(data)