import requests
import logging
import time
import uuid
from typing import Dict, Any, Optional, List
from config.settings import API_KEY, APP_ID

class JDYClient:
    """简道云API客户端 - v5版本"""
    
    def __init__(self):
        self.base_url = "https://api.jiandaoyun.com/api/v5"
        self.app_id = APP_ID
        self.api_key = API_KEY
        self.logger = logging.getLogger("JDYClient")
    
    def _make_auth_headers(self) -> Dict[str, str]:
        """生成认证头部"""
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }
    
    @staticmethod
    def _generate_transaction_id() -> str:
        """生成事务ID"""
        return str(uuid.uuid4())

    def request(self, method: str, endpoint: str, json_data: Optional[Dict] = None) -> Dict[str, Any]:
        """发送HTTP请求"""
        url = f"{self.base_url}{endpoint}"
        headers = self._make_auth_headers()
        
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=headers,
                json=json_data,
                timeout=30
            )
            
            self.logger.info(f"{method} {endpoint} -> {response.status_code}")
            
            if response.status_code >= 400:
                error_msg = response.text
                self.logger.error(f"API error {response.status_code}: {error_msg}")
                raise Exception(f"HTTP {response.status_code}: {error_msg[:200]}")
            
            # 直接返回JSON
            return response.json() if response.text else {}
                    
        except Exception as e:
            self.logger.error(f"请求失败: {str(e)}")
            raise

    def get_form_widgets(self, entry_id: str) -> Dict[str, Any]:
        """获取表单字段信息"""
        endpoint = "/app/entry/widget/list"
        payload = {
            "app_id": self.app_id,
            "entry_id": entry_id
        }
        return self.request('POST', endpoint, payload)

    def create_data(self, entry_id: str, data: Dict[str, Any], 
                   transaction_id: Optional[str] = None) -> str:
        """创建单条数据"""
        # 包装数据格式
        wrapped_data = {}
        for key, value in data.items():
            if isinstance(value, dict) and 'value' in value:
                wrapped_data[key] = value
            else:
                wrapped_data[key] = {'value': value}
        
        endpoint = "/app/entry/data/create"
        payload = {
            "app_id": self.app_id,
            "entry_id": entry_id,
            "data": wrapped_data,
            "is_start_trigger": False,
            "is_start_workflow": False
        }
        
        if not transaction_id:
            transaction_id = self._generate_transaction_id()
        payload["transaction_id"] = transaction_id
        
        result = self.request('POST', endpoint, payload)
        # 响应格式: {"data": {"_id": "xxx", ...}}
        return result.get('data', {}).get('_id', '')

    def query_data(self, entry_id: str, filters: Dict = None, limit: int = 100, 
                  data_id: str = None) -> List[Dict]:
        """查询数据"""
        endpoint = "/app/entry/data/list"
        payload = {
            "app_id": self.app_id,
            "entry_id": entry_id,
            "limit": limit
        }
        if data_id:
            payload["data_id"] = data_id
        if filters:
            payload["filter"] = filters
        result = self.request('POST', endpoint, payload)
        return result.get('data', [])

    def get_data(self, entry_id: str, data_id: str) -> Dict[str, Any]:
        """获取单条数据"""
        endpoint = "/app/entry/data/get"
        payload = {
            "app_id": self.app_id,
            "entry_id": entry_id,
            "data_id": data_id
        }
        return self.request('POST', endpoint, payload)

    def update_data(self, entry_id: str, data_id: str, data: Dict[str, Any],
                   transaction_id: Optional[str] = None) -> bool:
        """更新单条数据"""
        # 包装数据格式
        wrapped_data = {}
        for key, value in data.items():
            if isinstance(value, dict) and 'value' in value:
                wrapped_data[key] = value
            else:
                wrapped_data[key] = {'value': value}
        
        endpoint = "/app/entry/data/update"
        payload = {
            "app_id": self.app_id,
            "entry_id": entry_id,
            "data_id": data_id,
            "data": wrapped_data,
            "is_start_trigger": False
        }
        
        if not transaction_id:
            transaction_id = self._generate_transaction_id()
        payload["transaction_id"] = transaction_id
        
        self.request('POST', endpoint, payload)
        return True

    def delete_data(self, entry_id: str, data_id: str) -> bool:
        """删除单条数据"""
        endpoint = "/app/entry/data/delete"
        payload = {
            "app_id": self.app_id,
            "entry_id": entry_id,
            "data_id": data_id
        }
        self.request('POST', endpoint, payload)
        return True

    def batch_create_data(self, entry_id: str, data_list: List[Dict],
                         transaction_id: Optional[str] = None) -> List[str]:
        """批量创建数据"""
        wrapped_list = []
        for data in data_list:
            wrapped_data = {}
            for key, value in data.items():
                if isinstance(value, dict) and 'value' in value:
                    wrapped_data[key] = value
                else:
                    wrapped_data[key] = {'value': value}
            wrapped_list.append(wrapped_data)
        
        endpoint = "/app/entry/data/batch_create"
        payload = {
            "app_id": self.app_id,
            "entry_id": entry_id,
            "data_list": wrapped_list,
            "is_start_trigger": False,
            "is_start_workflow": False
        }
        
        if not transaction_id:
            transaction_id = self._generate_transaction_id()
        payload["transaction_id"] = transaction_id
        
        result = self.request('POST', endpoint, payload)
        # 响应格式: {"data": [{"_id": "xxx"}, ...]} 或 {"success_ids": [...]}
        if 'success_ids' in result:
            return result.get('success_ids', [])
        # 如果响应是data列表，提取_id
        data = result.get('data', [])
        return [item.get('_id') for item in data if item.get('_id')]

    def batch_update_data(self, entry_id: str, data_ids: List[str], 
                         data: Dict[str, Any], transaction_id: Optional[str] = None) -> bool:
        """批量更新数据"""
        wrapped_data = {}
        for key, value in data.items():
            if isinstance(value, dict) and 'value' in value:
                wrapped_data[key] = value
            else:
                wrapped_data[key] = {'value': value}
        
        endpoint = "/app/entry/data/batch_update"
        payload = {
            "app_id": self.app_id,
            "entry_id": entry_id,
            "data_ids": data_ids,
            "data": wrapped_data
        }
        
        if not transaction_id:
            transaction_id = self._generate_transaction_id()
        payload["transaction_id"] = transaction_id
        
        self.request('POST', endpoint, payload)
        return True

    def batch_delete_data(self, entry_id: str, data_ids: List[str]) -> bool:
        """批量删除数据"""
        endpoint = "/app/entry/data/batch_delete"
        payload = {
            "app_id": self.app_id,
            "entry_id": entry_id,
            "data_ids": data_ids
        }
        self.request('POST', endpoint, payload)
        return True