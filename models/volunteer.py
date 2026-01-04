from core.api_client import JDYClient
from config.settings import VOLUNTEER_ENTRY_ID
import pandas as pd
from typing import List, Dict, Any, Optional

class VolunteerModel:
    FORM_NAME = "义工档案"
    ENTRY_ID = VOLUNTEER_ENTRY_ID
    
    FIELD_NAME = "姓名"
    FIELD_PHONE = "手机号"
    FIELD_EMAIL = "邮箱"
    FIELD_AGE = "年龄"
    FIELD_GENDER = "性别"
    FIELD_ADDRESS = "住址"
    FIELD_EMERGENCY_CONTACT = "紧急联系人"
    FIELD_EMERGENCY_PHONE = "紧急联系电话"
    FIELD_SKILLS = "技能特长"
    FIELD_EXPERIENCE = "义工经验"
    FIELD_AVAILABLE_TIME = "可服务时间"
    FIELD_VOLUNTEER_TYPE = "义工类型"
    FIELD_JOIN_DATE = "加入日期"
    FIELD_STATUS = "状态"
    FIELD_TOTAL_HOURS = "累计工时"
    FIELD_REMARKS = "备注"
    
    @classmethod
    def create(cls, **data) -> str:
        """新增义工"""
        client = JDYClient()
        return client.create_data(cls.ENTRY_ID, data)
    
    @classmethod
    def get_by_id(cls, record_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取义工信息"""
        client = JDYClient()
        return client.get_data(cls.ENTRY_ID, record_id)
    
    @classmethod
    def update(cls, record_id: str, **data) -> bool:
        """更新义工信息"""
        client = JDYClient()
        return client.update_data(cls.ENTRY_ID, record_id, data)
    
    @classmethod
    def delete(cls, record_id: str) -> bool:
        """删除义工记录"""
        client = JDYClient()
        return client.delete_data(cls.ENTRY_ID, record_id)
    
    @classmethod
    def list_all(cls) -> pd.DataFrame:
        """获取所有义工列表"""
        client = JDYClient()
        data = client.query_data(cls.ENTRY_ID)
        return pd.DataFrame(data)
    
    @classmethod
    def list_by_status(cls, status: str) -> pd.DataFrame:
        """按状态筛选义工"""
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
        """按姓名搜索义工"""
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
    def get_volunteer_count(cls) -> int:
        """获取义工总数"""
        data = cls.list_all()
        return len(data)
    
    @classmethod
    def get_active_volunteers(cls) -> pd.DataFrame:
        """获取活跃义工列表"""
        return cls.list_by_status("活跃")