"""
寺院义工管理表单构建器
专为寺院义工招募、管理、活动报名等场景设计
"""
from typing import Dict, Any, List, Optional
from core.api_client import JDYClient

class TempleVolunteerFormBuilder:
    """寺院义工表单构建器"""
    
    def __init__(self):
        self.client = JDYClient()
        self.fields = []
        
    def add_text_field(self, name: str, label: str, required: bool = False, placeholder: str = "") -> 'FormBuilder':
        """添加文本字段"""
        field = {
            "name": name,
            "label": label,
            "type": "text",
            "required": required,
            "placeholder": placeholder
        }
        self.fields.append(field)
        return self
        
    def add_number_field(self, name: str, label: str, required: bool = False, min_value: Optional[int] = None, max_value: Optional[int] = None) -> 'FormBuilder':
        """添加数字字段"""
        field = {
            "name": name,
            "label": label,
            "type": "number",
            "required": required,
            "min": min_value,
            "max": max_value
        }
        self.fields.append(field)
        return self
        
    def add_date_field(self, name: str, label: str, required: bool = False, format_type: str = "YYYY-MM-DD") -> 'FormBuilder':
        """添加日期字段"""
        field = {
            "name": name,
            "label": label,
            "type": "date",
            "required": required,
            "format": format_type
        }
        self.fields.append(field)
        return self
        
    def add_select_field(self, name: str, label: str, options: List[str], required: bool = False, multiple: bool = False) -> 'FormBuilder':
        """添加选择字段"""
        field = {
            "name": name,
            "label": label,
            "type": "select" if not multiple else "multi_select",
            "required": required,
            "options": [{"label": opt, "value": opt} for opt in options]
        }
        self.fields.append(field)
        return self
        
    def add_textarea_field(self, name: str, label: str, required: bool = False, rows: int = 3) -> 'FormBuilder':
        """添加多行文本字段"""
        field = {
            "name": name,
            "label": label,
            "type": "textarea",
            "required": required,
            "rows": rows
        }
        self.fields.append(field)
        return self
        
    def add_phone_field(self, name: str, label: str, required: bool = False) -> 'FormBuilder':
        """添加手机号字段"""
        field = {
            "name": name,
            "label": label,
            "type": "phone",
            "required": required
        }
        self.fields.append(field)
        return self
        
    def add_email_field(self, name: str, label: str, required: bool = False) -> 'FormBuilder':
        """添加邮箱字段"""
        field = {
            "name": name,
            "label": label,
            "type": "email",
            "required": required
        }
        self.fields.append(field)
        return self
        
    def add_image_field(self, name: str, label: str, required: bool = False, max_count: int = 5) -> 'FormBuilder':
        """添加图片上传字段"""
        field = {
            "name": name,
            "label": label,
            "type": "image",
            "required": required,
            "maxCount": max_count
        }
        self.fields.append(field)
        return self
        
    def create_temple_volunteer_registration_form(self) -> str:
        """创建寺院义工注册表单"""
        self.fields = []
        form_data = {
            "name": "寺院义工注册",
            "description": "寺院义工信息登记表单",
            "widgets": [
                self.add_text_field("name", "姓名", required=True).fields[-1],
                self.add_select_field("gender", "性别", ["男", "女"], required=True).fields[-1],
                self.add_number_field("age", "年龄", required=True, min_value=18, max_value=70).fields[-1],
                self.add_phone_field("phone", "手机号码", required=True).fields[-1],
                self.add_text_field("wechat", "微信号").fields[-1],
                self.add_select_field("id_type", "证件类型", ["身份证", "护照", "军官证", "其他"], required=True).fields[-1],
                self.add_text_field("id_number", "证件号码", required=True).fields[-1],
                self.add_textarea_field("address", "常住地址", required=True).fields[-1],
                self.add_select_field("education", "文化程度", [
                    "小学", "初中", "高中", "大专", "本科", "硕士", "博士"
                ]).fields[-1],
                self.add_select_field("occupation", "职业", [
                    "学生", "教师", "医生", "工程师", "公务员", "企业家", 
                    "自由职业", "退休", "其他"
                ]).fields[-1],
                self.add_select_field("religious_affiliation", "宗教信仰", [
                    "佛教", "道教", "基督教", "伊斯兰教", "无", "其他"
                ]).fields[-1],
                self.add_select_field("volunteer_type", "义工类型", [
                    "日常义工", "法会义工", "接待义工", "清洁义工", 
                    "园艺义工", "文书义工", "摄影义工", "医疗义工"
                ], multiple=True, required=True).fields[-1],
                self.add_select_field("available_days", "可服务时间", [
                    "周一", "周二", "周三", "周四", "周五", "周六", "周日"
                ], multiple=True, required=True).fields[-1],
                self.add_select_field("available_time", "可服务时段", [
                    "上午(8:00-12:00)", "下午(14:00-18:00)", "晚上(19:00-21:00)"
                ], multiple=True).fields[-1],
                self.add_textarea_field("skills", "特长技能描述").fields[-1],
                self.add_textarea_field("experience", "相关义工经验").fields[-1],
                self.add_select_field("emergency_contact_relation", "紧急联系人关系", [
                    "配偶", "父母", "子女", "兄弟姐妹", "朋友", "其他"
                ]).fields[-1],
                self.add_text_field("emergency_contact_name", "紧急联系人姓名").fields[-1],
                self.add_phone_field("emergency_contact_phone", "紧急联系人电话").fields[-1],
                self.add_textarea_field("health_condition", "健康状况说明").fields[-1],
                self.add_select_field("dietary_preference", "饮食偏好", [
                    "素食", "荤素皆可", "清真", "其他"
                ]).fields[-1],
                self.add_image_field("id_photo", "证件照片").fields[-1],
                self.add_image_field("avatar", "个人近照").fields[-1]
            ]
        }
        
        return self.client.create_form(form_data)
        
    def create_temple_activity_registration_form(self) -> str:
        """创建寺院活动报名表单"""
        self.fields = []
        form_data = {
            "name": "寺院活动报名",
            "description": "寺院法会、讲座等活动报名表单",
            "widgets": [
                self.add_text_field("volunteer_name", "义工姓名", required=True).fields[-1],
                self.add_phone_field("volunteer_phone", "联系电话", required=True).fields[-1],
                self.add_select_field("activity_type", "活动类型", [
                    "早课", "晚课", "法会", "讲经", "禅修", "供灯", 
                    "放生", "供僧", "寺院清洁", "园艺维护", "接待引导"
                ], required=True).fields[-1],
                self.add_text_field("activity_name", "活动名称", required=True).fields[-1],
                self.add_date_field("activity_date", "活动日期", required=True).fields[-1],
                self.add_select_field("activity_time", "活动时间", [
                    "5:00-7:00", "8:00-10:00", "10:00-12:00", 
                    "14:00-16:00", "16:00-18:00", "19:00-21:00"
                ], required=True).fields[-1],
                self.add_select_field("role", "报名角色", [
                    "参与者", "义工", "护持", "接待", "摄影", "后勤"
                ], required=True).fields[-1],
                self.add_number_field("participants", "同行人数", min_value=0, max_value=20).fields[-1],
                self.add_select_field("transportation", "交通方式", [
                    "自驾", "公交", "地铁", "步行", "拼车"
                ]).fields[-1],
                self.add_select_field("dietary_requirement", "饮食需求", [
                    "素食", "无特殊要求", "清真", "过敏备注"
                ]).fields[-1],
                self.add_textarea_field("special_needs", "特殊需求说明").fields[-1],
                self.add_textarea_field("karmic_connection", "与寺院因缘").fields[-1]
            ]
        }
        
        return self.client.create_form(form_data)
        
    def create_temple_feedback_form(self) -> str:
        """创建寺院活动反馈表单"""
        self.fields = []
        form_data = {
            "name": "寺院活动反馈",
            "description": "寺院法会、活动参与反馈表单",
            "widgets": [
                self.add_text_field("volunteer_name", "义工姓名", required=True).fields[-1],
                self.add_phone_field("volunteer_phone", "联系电话").fields[-1],
                self.add_select_field("activity_type", "活动类型", [
                    "早课", "晚课", "法会", "讲经", "禅修", "供灯", 
                    "放生", "供僧", "寺院清洁", "其他"
                ], required=True).fields[-1],
                self.add_text_field("activity_name", "活动名称", required=True).fields[-1],
                self.add_date_field("activity_date", "活动日期", required=True).fields[-1],
                self.add_select_field("participation_role", "参与角色", [
                    "参与者", "义工", "护持", "接待", "摄影", "后勤"
                ], required=True).fields[-1],
                self.add_select_field("satisfaction", "整体满意度", [
                    "非常满意", "满意", "一般", "需改进"
                ], required=True).fields[-1],
                self.add_select_field("spiritual_benefit", "心灵收获", [
                    "很大", "较大", "一般", "较小"
                ]).fields[-1],
                self.add_select_field("service_quality", "服务质量", [
                    "非常好", "好", "一般", "需改进"
                ]).fields[-1],
                self.add_select_field("environment", "环境氛围", [
                    "非常好", "好", "一般", "需改进"
                ]).fields[-1],
                self.add_textarea_field("experience", "参与体验", required=True).fields[-1],
                self.add_textarea_field("suggestions", "改进建议").fields[-1],
                self.add_textarea_field("dharma_gain", "佛法收获分享").fields[-1],
                self.add_select_field("recommend", "是否推荐给他人", [
                    "会推荐", "可能会", "不会推荐"
                ]).fields[-1],
                self.add_image_field("photos", "活动照片", max_count=5).fields[-1]
            ]
        }
        
        return self.client.create_form(form_data)
        
    def create_custom_form(self, name: str, description: str = "") -> str:
        """创建自定义表单"""
        form_data = {
            "name": name,
            "description": description,
            "widgets": self.fields
        }
        
        return self.client.create_form(form_data)