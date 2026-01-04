# 职责：活动库的CRUD，管理寺院活动信息
from core.api_client import JDYClient
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime

class EventModel:
    # 表单名称
    FORM_NAME = "活动库"
    
    # 字段常量定义
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
    
    def __init__(self):
        self.client = JDYClient()
        self.form_id = None
    
    @classmethod
    def create_form(cls) -> str:
        """创建活动库表单"""
        client = JDYClient()
        
        # 定义表单配置
        form_data = {
            "name": cls.FORM_NAME,
            "widgets": [
                {
                    "type": "text",
                    "name": cls.FIELD_EVENT_NAME,
                    "label": "活动名称",
                    "required": True
                },
                {
                    "type": "select",
                    "name": cls.FIELD_EVENT_TYPE,
                    "label": "活动类型",
                    "required": True,
                    "options": [
                        "日常法务",
                        "法会活动",
                        "接待活动",
                        "清洁活动",
                        "园艺活动",
                        "文书工作",
                        "摄影记录",
                        "医疗服务",
                        "其他"
                    ]
                },
                {
                    "type": "date",
                    "name": cls.FIELD_EVENT_DATE,
                    "label": "活动日期",
                    "required": True
                },
                {
                    "type": "time",
                    "name": cls.FIELD_START_TIME,
                    "label": "开始时间",
                    "required": True
                },
                {
                    "type": "time",
                    "name": cls.FIELD_END_TIME,
                    "label": "结束时间",
                    "required": True
                },
                {
                    "type": "text",
                    "name": cls.FIELD_LOCATION,
                    "label": "活动地点",
                    "required": True
                },
                {
                    "type": "textarea",
                    "name": cls.FIELD_DESCRIPTION,
                    "label": "活动描述",
                    "placeholder": "请详细描述活动内容、目的和注意事项",
                    "required": False
                },
                {
                    "type": "number",
                    "name": cls.FIELD_REQUIRED_VOLUNTEERS,
                    "label": "需要义工人数",
                    "required": True,
                    "min": 1,
                    "max": 50
                },
                {
                    "type": "select",
                    "name": cls.FIELD_REQUIRED_SKILLS,
                    "label": "所需技能",
                    "required": False,
                    "options": [
                        "无特殊要求",
                        "医疗知识",
                        "摄影技术",
                        "文书处理",
                        "翻译能力",
                        "烹饪技能",
                        "园艺技能",
                        "接待经验",
                        "其他专业技能"
                    ],
                    "multiple": True
                },
                {
                    "type": "text",
                    "name": cls.FIELD_CONTACT_PERSON,
                    "label": "联系人姓名",
                    "required": True
                },
                {
                    "type": "phone",
                    "name": cls.FIELD_CONTACT_PHONE,
                    "label": "联系电话",
                    "required": True
                },
                {
                    "type": "select",
                    "name": cls.FIELD_STATUS,
                    "label": "活动状态",
                    "required": True,
                    "options": [
                        "计划中",
                        "报名中",
                        "进行中",
                        "已完成",
                        "已取消"
                    ],
                    "default": "计划中"
                },
                {
                    "type": "date",
                    "name": cls.FIELD_REGISTRATION_DEADLINE,
                    "label": "报名截止日",
                    "required": True
                },
                {
                    "type": "number",
                    "name": cls.FIELD_MAX_PARTICIPANTS,
                    "label": "最大参与人数",
                    "required": True,
                    "min": 1,
                    "max": 100
                },
                {
                    "type": "number",
                    "name": cls.FIELD_CURRENT_PARTICIPANTS,
                    "label": "当前参与人数",
                    "default": 0,
                    "min": 0,
                    "required": False
                },
                {
                    "type": "textarea",
                    "name": cls.FIELD_NOTES,
                    "label": "备注",
                    "required": False
                }
            ]
        }
        
        try:
            form_id = client.create_form(form_data)
            print(f"✅ 活动库表单创建成功: {form_id}")
            return form_id
        except Exception as e:
            print(f"❌ 创建活动库表单失败: {str(e)}")
            raise
    
    @classmethod
    def create(cls, **data) -> Dict[str, Any]:
        """创建新活动"""
        client = JDYClient()
        return client.add_record(cls.FORM_NAME, data)
    
    @classmethod
    def get_by_id(cls, record_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取活动信息"""
        client = JDYClient()
        return client.get_record(cls.FORM_NAME, record_id)
    
    @classmethod
    def update(cls, record_id: str, **data) -> Dict[str, Any]:
        """更新活动信息"""
        client = JDYClient()
        return client.update_record(cls.FORM_NAME, record_id, data)
    
    @classmethod
    def delete(cls, record_id: str) -> bool:
        """删除活动记录"""
        client = JDYClient()
        return client.delete_record(cls.FORM_NAME, record_id)
    
    @classmethod
    def list_all(cls) -> pd.DataFrame:
        """获取所有活动列表"""
        client = JDYClient()
        data = client.get_records(cls.FORM_NAME)
        return pd.DataFrame(data)
    
    @classmethod
    def list_by_type(cls, event_type: str) -> pd.DataFrame:
        """按活动类型筛选"""
        client = JDYClient()
        data = client.get_records(cls.FORM_NAME, {cls.FIELD_EVENT_TYPE: event_type})
        return pd.DataFrame(data)
    
    @classmethod
    def list_by_status(cls, status: str) -> pd.DataFrame:
        """按活动状态筛选"""
        client = JDYClient()
        data = client.get_records(cls.FORM_NAME, {cls.FIELD_STATUS: status})
        return pd.DataFrame(data)
    
    @classmethod
    def list_upcoming_events(cls) -> pd.DataFrame:
        """获取即将进行的活动"""
        client = JDYClient()
        today = datetime.now().strftime("%Y-%m-%d")
        data = client.get_records(cls.FORM_NAME, {
            cls.FIELD_EVENT_DATE: f">={today}",
            cls.FIELD_STATUS: "报名中"
        })
        return pd.DataFrame(data)
    
    @classmethod
    def search_by_name(cls, name: str) -> pd.DataFrame:
        """按活动名称搜索"""
        client = JDYClient()
        data = client.get_records(cls.FORM_NAME, {cls.FIELD_EVENT_NAME: name})
        return pd.DataFrame(data)
    
    @classmethod
    def get_event_count(cls) -> int:
        """获取活动总数"""
        client = JDYClient()
        return client.get_record_count(cls.FORM_NAME)
    
    @classmethod
    def get_events_by_date_range(cls, start_date: str, end_date: str) -> pd.DataFrame:
        """获取指定日期范围内的活动"""
        client = JDYClient()
        data = client.get_records(cls.FORM_NAME, {
            cls.FIELD_EVENT_DATE: f">={start_date}",
            f"{cls.FIELD_EVENT_DATE}_end": f"<={end_date}"
        })
        return pd.DataFrame(data)