"""
寺院义工管理仪表盘构建器
专为寺院义工数据统计和管理场景设计
"""
from typing import Dict, List, Optional
from core.api_client import JDYClient

class TempleVolunteerDashboardBuilder:
    """寺院义工仪表盘构建器"""
    
    def __init__(self):
        self.client = JDYClient()
        self.widgets = []
        
    def add_chart_widget(self, title: str, chart_type: str, data_source: str, 
                        x_field: str, y_field: str, filters: Optional[Dict] = None) -> 'TempleVolunteerDashboardBuilder':
        """添加图表组件"""
        widget = {
            "type": "chart",
            "title": title,
            "chartType": chart_type,
            "dataSource": data_source,
            "xField": x_field,
            "yField": y_field,
            "filters": filters or {}
        }
        self.widgets.append(widget)
        return self
        
    def add_stat_widget(self, title: str, data_source: str, field: str, 
                       operation: str = "count", filters: Optional[Dict] = None) -> 'TempleVolunteerDashboardBuilder':
        """添加统计组件"""
        widget = {
            "type": "stat",
            "title": title,
            "dataSource": data_source,
            "field": field,
            "operation": operation,
            "filters": filters or {}
        }
        self.widgets.append(widget)
        return self
        
    def add_table_widget(self, title: str, data_source: str, fields: List[str], 
                        page_size: int = 10, filters: Optional[Dict] = None) -> 'TempleVolunteerDashboardBuilder':
        """添加表格组件"""
        widget = {
            "type": "table",
            "title": title,
            "dataSource": data_source,
            "fields": fields,
            "pageSize": page_size,
            "filters": filters or {}
        }
        self.widgets.append(widget)
        return self
        
    def create_temple_volunteer_dashboard(self, volunteer_form_id: str, activity_form_id: str, feedback_form_id: str) -> str:
        """创建寺院义工管理仪表盘"""
        widgets = [
            {
                "type": "stat",
                "title": "总义工人数",
                "dataSource": volunteer_form_id,
                "field": "name",
                "operation": "count"
            },
            {
                "type": "stat",
                "title": "本月法务活动",
                "dataSource": activity_form_id,
                "field": "activity_name",
                "operation": "count"
            },
            {
                "type": "stat",
                "title": "平均满意度",
                "dataSource": feedback_form_id,
                "field": "satisfaction",
                "operation": "count"
            },
            {
                "type": "chart",
                "title": "义工年龄分布",
                "chartType": "pie",
                "dataSource": volunteer_form_id,
                "xField": "age",
                "yField": "count"
            },
            {
                "type": "chart",
                "title": "义工类型分布",
                "chartType": "bar",
                "dataSource": volunteer_form_id,
                "xField": "volunteer_type",
                "yField": "count"
            },
            {
                "type": "table",
                "title": "最近法务活动报名",
                "dataSource": activity_form_id,
                "fields": ["volunteer_name", "activity_name", "activity_date", "role"],
                "pageSize": 10
            }
        ]
        
        dashboard_data = {
            "name": "寺院义工管理仪表盘",
            "description": "寺院义工数据统计和法务活动总览",
            "widgets": widgets
        }
        return self.client.create_dashboard(dashboard_data)
        
    def create_temple_activity_dashboard(self, activity_form_id: str, feedback_form_id: str) -> str:
        """创建寺院法务活动管理仪表盘"""
        widgets = [
            {
                "type": "stat",
                "title": "总报名人数",
                "dataSource": activity_form_id,
                "field": "volunteer_name",
                "operation": "count"
            },
            {
                "type": "stat",
                "title": "本月法务活动",
                "dataSource": activity_form_id,
                "field": "activity_name",
                "operation": "count"
            },
            {
                "type": "stat",
                "title": "反馈总数",
                "dataSource": feedback_form_id,
                "field": "experience",
                "operation": "count"
            },
            {
                "type": "chart",
                "title": "法务活动类型分布",
                "chartType": "pie",
                "dataSource": activity_form_id,
                "xField": "activity_type",
                "yField": "count"
            },
            {
                "type": "chart",
                "title": "参与角色分布",
                "chartType": "bar",
                "dataSource": activity_form_id,
                "xField": "role",
                "yField": "count"
            }
        ]
        
        dashboard_data = {
            "name": "寺院法务活动管理",
            "description": "寺院法务活动数据统计分析",
            "widgets": widgets
        }
        return self.client.create_dashboard(dashboard_data)
        
    def create_temple_volunteer_analysis_dashboard(self, volunteer_form_id: str, activity_form_id: str) -> str:
        """创建寺院义工综合分析仪表盘"""
        widgets = [
            {
                "type": "stat",
                "title": "活跃义工人数",
                "dataSource": activity_form_id,
                "field": "volunteer_name",
                "operation": "distinctCount"
            },
            {
                "type": "stat",
                "title": "人均参与法务活动",
                "dataSource": activity_form_id,
                "field": "volunteer_name",
                "operation": "count"
            },
            {
                "type": "chart",
                "title": "义工年龄结构",
                "chartType": "pie",
                "dataSource": volunteer_form_id,
                "xField": "age",
                "yField": "count"
            },
            {
                "type": "chart",
                "title": "义工类型分布",
                "chartType": "bar",
                "dataSource": volunteer_form_id,
                "xField": "volunteer_type",
                "yField": "count"
            },
            {
                "type": "table",
                "title": "优秀义工排行",
                "dataSource": activity_form_id,
                "fields": ["volunteer_name", "activity_name", "activity_date", "role"],
                "pageSize": 10
            }
        ]
        
        dashboard_data = {
            "name": "寺院义工综合分析",
            "description": "寺院义工参与度、法务活动效果综合分析",
            "widgets": widgets
        }
        return self.client.create_dashboard(dashboard_data)
        
    def create_custom_dashboard(self, name: str, description: str = "") -> str:
        """创建自定义仪表盘"""
        dashboard_data = {
            "name": name,
            "description": description,
            "widgets": self.widgets
        }
        return self.client.create_dashboard(dashboard_data)