from core.api_client import JDYClient
from config.settings import VOLUNTEER_ENTRY_ID
import pandas as pd
from typing import List, Dict, Any, Optional

class VolunteerModel:
    FORM_NAME = "义工档案"
    ENTRY_ID = VOLUNTEER_ENTRY_ID
    
    # 字段映射到 widget ID
    FIELD_NAME = "_widget_1767515266471"                # 姓名
    FIELD_PHONE = "_widget_1767515266472"               # 手机号
    FIELD_ID_CARD = "_widget_1767516573304"             # 身份证号码
    FIELD_AGE = "_widget_1767515266474"                 # 年龄
    FIELD_GENDER = "_widget_1767515266475"              # 性别
    FIELD_SKILLS = "_widget_1767520662777"              # 技能特长（复选框）
    FIELD_AREA = "_widget_1767515266480"                # 常住区域
    FIELD_AVAILABLE_TIME = "_widget_1767515266482"      # 可服务时段（多选）
    FIELD_IS_ORDAINED = "_widget_1767516573307"         # 是否皈依
    FIELD_ORDAINED_DATE = "_widget_1767516573309"       # 皈依日期
    FIELD_DHARMA_NAME = "_widget_1767516573310"         # 法号
    FIELD_JOIN_DATE = "_widget_1767516573312"           # 加入日期
    FIELD_STATUS = "_widget_1767516573296"              # 状态
    FIELD_REMARKS = "_widget_1767516573315"             # 备注
    
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