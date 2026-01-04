# 职责：排班签到的CRUD，管理义工排班和签到记录
from core.api_client import JDYClient
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime

class ScheduleModel:
    # 表单名称
    FORM_NAME = "排班签到"
    
    # 字段常量定义
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
    
    def __init__(self):
        self.client = JDYClient()
        self.form_id = None
    
    @classmethod
    def create_form(cls) -> str:
        """创建排班签到表单"""
        client = JDYClient()
        
        # 定义表单配置
        form_data = {
            "name": cls.FORM_NAME,
            "widgets": [
                {
                    "type": "text",
                    "name": cls.FIELD_VOLUNTEER_NAME,
                    "label": "义工姓名",
                    "required": True
                },
                {
                    "type": "phone",
                    "name": cls.FIELD_VOLUNTEER_PHONE,
                    "label": "义工电话",
                    "required": True
                },
                {
                    "type": "text",
                    "name": cls.FIELD_EVENT_NAME,
                    "label": "活动名称",
                    "required": True
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
                    "type": "select",
                    "name": cls.FIELD_ROLE,
                    "label": "担任角色",
                    "required": True,
                    "options": [
                        "负责人",
                        "协助人",
                        "接待员",
                        "清洁员",
                        "摄影员",
                        "医疗员",
                        "文书员",
                        "其他"
                    ]
                },
                {
                    "type": "select",
                    "name": cls.FIELD_STATUS,
                    "label": "签到状态",
                    "required": True,
                    "options": [
                        "已排班",
                        "已确认",
                        "已签到",
                        "已签退",
                        "缺席",
                        "取消"
                    ],
                    "default": "已排班"
                },
                {
                    "type": "datetime",
                    "name": cls.FIELD_CHECK_IN_TIME,
                    "label": "签到时间",
                    "required": False
                },
                {
                    "type": "datetime",
                    "name": cls.FIELD_CHECK_OUT_TIME,
                    "label": "签退时间",
                    "required": False
                },
                {
                    "type": "number",
                    "name": cls.FIELD_ACTUAL_HOURS,
                    "label": "实际工时",
                    "min": 0,
                    "max": 24,
                    "required": False
                },
                {
                    "type": "textarea",
                    "name": cls.FIELD_REMARKS,
                    "label": "备注",
                    "required": False
                },
                {
                    "type": "date",
                    "name": cls.FIELD_SCHEDULE_DATE,
                    "label": "排班日期",
                    "default": "today",
                    "required": True
                },
                {
                    "type": "text",
                    "name": cls.FIELD_CONTACT_PERSON,
                    "label": "联系人",
                    "required": True
                }
            ]
        }
        
        try:
            form_id = client.create_form(form_data)
            print(f"✅ 排班签到表单创建成功: {form_id}")
            return form_id
        except Exception as e:
            print(f"❌ 创建排班签到表单失败: {str(e)}")
            raise
    
    @classmethod
    def create(cls, **data) -> Dict[str, Any]:
        """创建排班记录"""
        client = JDYClient()
        return client.add_record(cls.FORM_NAME, data)
    
    @classmethod
    def get_by_id(cls, record_id: str) -> Optional[Dict[str, Any]]:
        """根据ID获取排班记录"""
        client = JDYClient()
        return client.get_record(cls.FORM_NAME, record_id)
    
    @classmethod
    def update(cls, record_id: str, **data) -> Dict[str, Any]:
        """更新排班记录"""
        client = JDYClient()
        return client.update_record(cls.FORM_NAME, record_id, data)
    
    @classmethod
    def delete(cls, record_id: str) -> bool:
        """删除排班记录"""
        client = JDYClient()
        return client.delete_record(cls.FORM_NAME, record_id)
    
    @classmethod
    def list_all(cls) -> pd.DataFrame:
        """获取所有排班记录"""
        client = JDYClient()
        data = client.get_records(cls.FORM_NAME)
        return pd.DataFrame(data)
    
    @classmethod
    def list_by_volunteer(cls, volunteer_name: str) -> pd.DataFrame:
        """获取指定义工的排班记录"""
        client = JDYClient()
        data = client.get_records(cls.FORM_NAME, {cls.FIELD_VOLUNTEER_NAME: volunteer_name})
        return pd.DataFrame(data)
    
    @classmethod
    def list_by_event(cls, event_name: str) -> pd.DataFrame:
        """获取指定活动的排班记录"""
        client = JDYClient()
        data = client.get_records(cls.FORM_NAME, {cls.FIELD_EVENT_NAME: event_name})
        return pd.DataFrame(data)
    
    @classmethod
    def list_by_date(cls, event_date: str) -> pd.DataFrame:
        """获取指定日期的排班记录"""
        client = JDYClient()
        data = client.get_records(cls.FORM_NAME, {cls.FIELD_EVENT_DATE: event_date})
        return pd.DataFrame(data)
    
    @classmethod
    def list_by_status(cls, status: str) -> pd.DataFrame:
        """按签到状态筛选"""
        client = JDYClient()
        data = client.get_records(cls.FORM_NAME, {cls.FIELD_STATUS: status})
        return pd.DataFrame(data)
    
    @classmethod
    def list_upcoming_schedules(cls) -> pd.DataFrame:
        """获取即将进行的排班"""
        client = JDYClient()
        today = datetime.now().strftime("%Y-%m-%d")
        data = client.get_records(cls.FORM_NAME, {
            cls.FIELD_EVENT_DATE: f">={today}"
        })
        return pd.DataFrame(data)
    
    @classmethod
    def check_in(cls, record_id: str) -> Dict[str, Any]:
        """义工签到"""
        check_in_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return cls.update(record_id, 
                         **{cls.FIELD_STATUS: "已签到",
                            cls.FIELD_CHECK_IN_TIME: check_in_time})
    
    @classmethod
    def check_out(cls, record_id: str, actual_hours: float = None) -> Dict[str, Any]:
        """义工签退"""
        check_out_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        update_data = {
            cls.FIELD_STATUS: "已签退",
            cls.FIELD_CHECK_OUT_TIME: check_out_time
        }
        
        if actual_hours is not None:
            update_data[cls.FIELD_ACTUAL_HOURS] = actual_hours
        else:
            # 计算实际工时（基于签到和签退时间）
            record = cls.get_by_id(record_id)
            if record and cls.FIELD_CHECK_IN_TIME in record:
                # 这里简化处理，实际应用中需要更精确的计算
                update_data[cls.FIELD_ACTUAL_HOURS] = 2.0  # 默认2小时
        
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
        client = JDYClient()
        return client.get_record_count(cls.FORM_NAME)
    
    @classmethod
    def get_volunteer_schedule_count(cls, volunteer_name: str) -> int:
        """获取义工参与次数"""
        schedules = cls.list_by_volunteer(volunteer_name)
        return len(schedules)