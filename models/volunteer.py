# 职责：义工档案的CRUD，字段名做常量管理
from core.api_client import JDYClient
import pandas as pd
from typing import List, Dict, Any, Optional

class VolunteerModel:
    # 表单名称
    FORM_NAME = "义工档案"
    
    # 字段常量定义
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
    
    def __init__(self):
        self.client = JDYClient()
        self.form_id = None
    
    @classmethod
    def create_form(cls) -> str:
        """创建义工档案表单"""
        client = JDYClient()
        
        # 定义表单配置
        form_data = {
            "name": cls.FORM_NAME,
            "widgets": [
                {
                    "type": "text",
                    "name": cls.FIELD_NAME,
                    "label": "义工姓名",
                    "required": True
                },
                {
                    "type": "phone",
                    "name": cls.FIELD_PHONE,
                    "label": "手机号码",
                    "required": True
                },
                {
                    "type": "email",
                    "name": cls.FIELD_EMAIL,
                    "label": "邮箱地址",
                    "required": False
                },
                {
                    "type": "number",
                    "name": cls.FIELD_AGE,
                    "label": "年龄",
                    "required": True,
                    "min": 16,
                    "max": 80
                },
                {
                    "type": "select",
                    "name": cls.FIELD_GENDER,
                    "label": "性别",
                    "required": True,
                    "options": ["男", "女"]
                },
                {
                    "type": "text",
                    "name": cls.FIELD_ADDRESS,
                    "label": "住址",
                    "required": False
                },
                {
                    "type": "text",
                    "name": cls.FIELD_EMERGENCY_CONTACT,
                    "label": "紧急联系人姓名",
                    "required": True
                },
                {
                    "type": "phone",
                    "name": cls.FIELD_EMERGENCY_PHONE,
                    "label": "紧急联系电话",
                    "required": True
                },
                {
                    "type": "textarea",
                    "name": cls.FIELD_SKILLS,
                    "label": "技能特长",
                    "placeholder": "如：医疗、摄影、翻译、烹饪等",
                    "required": False
                },
                {
                    "type": "textarea",
                    "name": cls.FIELD_EXPERIENCE,
                    "label": "义工经验",
                    "placeholder": "请简述过往的义工服务经历",
                    "required": False
                },
                {
                    "type": "select",
                    "name": cls.FIELD_AVAILABLE_TIME,
                    "label": "可服务时间",
                    "required": True,
                    "options": [
                        "工作日白天",
                        "工作日晚上",
                        "周末白天",
                        "周末晚上",
                        "随时可参与"
                    ],
                    "multiple": True
                },
                {
                    "type": "select",
                    "name": cls.FIELD_VOLUNTEER_TYPE,
                    "label": "义工类型",
                    "required": True,
                    "options": [
                        "日常义工",
                        "法会义工",
                        "接待义工",
                        "清洁义工",
                        "园艺义工",
                        "文书义工",
                        "摄影义工",
                        "医疗义工"
                    ],
                    "multiple": True
                },
                {
                    "type": "date",
                    "name": cls.FIELD_JOIN_DATE,
                    "label": "加入日期",
                    "default": "today",
                    "required": True
                },
                {
                    "type": "select",
                    "name": cls.FIELD_STATUS,
                    "label": "状态",
                    "required": True,
                    "options": ["活跃", "暂停", "退出"],
                    "default": "活跃"
                },
                {
                    "type": "number",
                    "name": cls.FIELD_TOTAL_HOURS,
                    "label": "累计工时",
                    "default": 0,
                    "min": 0,
                    "required": False
                },
                {
                    "type": "textarea",
                    "name": cls.FIELD_REMARKS,
                    "label": "备注",
                    "required": False
                }
            ]
        }
        
        try:
            form_id = client.create_form(form_data)
            print(f"✅ 义工档案表单创建成功: {form_id}")
            return form_id
        except Exception as e:
            print(f"❌ 创建义工档案表单失败: {str(e)}")
            raise
    
    @classmethod
    def create(cls, **data) -> Dict[str, Any]:
        """新增义工"""
        client = JDYClient()
        return client.add_record(cls.FORM_NAME, data)
    
    @classmethod
    def get_by_id(cls, record_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取义工信息"""
        client = JDYClient()
        return client.get_record(cls.FORM_NAME, record_id)
    
    @classmethod
    def update(cls, record_id: str, **data) -> Dict[str, Any]:
        """更新义工信息"""
        client = JDYClient()
        return client.update_record(cls.FORM_NAME, record_id, data)
    
    @classmethod
    def delete(cls, record_id: str) -> bool:
        """删除义工记录"""
        client = JDYClient()
        return client.delete_record(cls.FORM_NAME, record_id)
    
    @classmethod
    def list_all(cls) -> pd.DataFrame:
        """获取所有义工列表"""
        client = JDYClient()
        data = client.get_records(cls.FORM_NAME)
        return pd.DataFrame(data)
    
    @classmethod
    def list_by_skill(cls, skill: str) -> pd.DataFrame:
        """按技能筛选，返回DataFrame"""
        client = JDYClient()
        data = client.get_records(cls.FORM_NAME, {cls.FIELD_SKILLS: skill})
        return pd.DataFrame(data)
    
    @classmethod
    def list_by_status(cls, status: str) -> pd.DataFrame:
        """按状态筛选义工"""
        client = JDYClient()
        data = client.get_records(cls.FORM_NAME, {cls.FIELD_STATUS: status})
        return pd.DataFrame(data)
    
    @classmethod
    def list_by_volunteer_type(cls, volunteer_type: str) -> pd.DataFrame:
        """按义工类型筛选"""
        client = JDYClient()
        data = client.get_records(cls.FORM_NAME, {cls.FIELD_VOLUNTEER_TYPE: volunteer_type})
        return pd.DataFrame(data)
    
    @classmethod
    def search_by_name(cls, name: str) -> pd.DataFrame:
        """按姓名搜索义工"""
        client = JDYClient()
        data = client.get_records(cls.FORM_NAME, {cls.FIELD_NAME: name})
        return pd.DataFrame(data)
    
    @classmethod
    def get_volunteer_count(cls) -> int:
        """获取义工总数"""
        client = JDYClient()
        return client.get_record_count(cls.FORM_NAME)
    
    @classmethod
    def get_active_volunteers(cls) -> pd.DataFrame:
        """获取活跃义工列表"""
        return cls.list_by_status("活跃")