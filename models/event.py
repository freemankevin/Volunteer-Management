from core.api_client import JDYClient
from config.settings import EVENT_ENTRY_ID
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime

class EventModel:
    FORM_NAME = "活动库"
    ENTRY_ID = EVENT_ENTRY_ID
    
    # 字段映射到 widget ID
    FIELD_EVENT_NAME = "_widget_1767519959682"           # 活动名称
    FIELD_EVENT_TYPE = "_widget_1767519959684"           # 活动类型
    FIELD_DESCRIPTION = "_widget_1767519959687"          # 活动描述
    FIELD_EVENT_DATE = "_widget_1767519959689"           # 活动日期
    FIELD_START_TIME = "_widget_1767519959690"           # 开始时间
    FIELD_END_TIME = "_widget_1767519959691"             # 结束时间
    FIELD_LOCATION = "_widget_1767519959693"             # 活动地点
    FIELD_REQUIRED_VOLUNTEERS = "_widget_1767519959695"  # 需要义工人数
    FIELD_CURRENT_PARTICIPANTS = "_widget_1767519959696" # 当前报名人数
    FIELD_STATUS = "_widget_1767519959699"               # 活动状态
    FIELD_REQUIRED_SKILLS = "_widget_1767519959703"      # 所需技能（复选框）
    FIELD_REMARKS = "_widget_1767519959705"              # 备注
    
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