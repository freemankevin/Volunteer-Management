# core/api_client.py - 适配简道云v5 API格式
import requests
import logging
import time
from typing import Dict, Any, Optional, List
from config.settings import API_KEY, APP_ID

class JDYClient:
    """简道云API客户端 - v5版本"""
    
    def __init__(self):
        # 使用 v5 API 根据官方文档
        self.base_url = "https://api.jiandaoyun.com/api/v5"
        self.app_id = APP_ID
        self.api_key = API_KEY
        self.logger = logging.getLogger("JDYClient")
    
    def _make_auth_headers(self) -> Dict[str, str]:
        """
        生成认证头部 - 简道云格式
        根据官方文档：https://hc.jiandaoyun.com/open/12047
        使用 Authorization: Bearer YOUR_APIKEY
        """
        return {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.api_key}'
        }

    def request(self, method: str, endpoint: str, json_data: Optional[Dict] = None, 
                retries: int = 3) -> Dict[str, Any]:
        """发送HTTP请求，带重试"""
        url = f"{self.base_url}{endpoint}"
        headers = self._make_auth_headers()
        
        for attempt in range(retries):
            try:
                response = requests.request(
                    method=method,
                    url=url,
                    headers=headers,
                    json=json_data,
                    timeout=30
                )
                
                self.logger.info(f"{method} {endpoint} -> {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        result = response.json()
                        # 简道云返回格式：{"code": 0, "msg": "success", "data": {...}}
                        if result.get('code') == 0:
                            return result.get('data', {})
                        else:
                            raise Exception(f"API error: {result.get('msg', '未知错误')}")
                    except ValueError as e:
                        # 响应不是JSON
                        self.logger.error(f"响应不是JSON格式: {response.text[:200]}")
                        raise Exception(f"响应格式错误: {str(e)}")
                elif response.status_code == 403:
                    raise Exception("403 权限被拒绝 - API密钥或签名有误")
                elif response.status_code == 404:
                    raise Exception("404 找不到资源 - 检查APP_ID是否正确")
                else:
                    raise Exception(f"HTTP {response.status_code}: {response.text[:100]}")
                    
            except Exception as e:
                self.logger.error(f"请求失败 (尝试 {attempt + 1}/{retries}): {str(e)}")
                if attempt == retries - 1:
                    raise
                time.sleep(2 ** attempt)

    def get_form_widgets(self, entry_id: str) -> Dict[str, Any]:
        """获取表单字段信息"""
        endpoint = "/app/entry/widgets/get"
        payload = {
            "app_id": self.app_id,
            "entry_id": entry_id
        }
        return self.request('POST', endpoint, payload)

    def create_data(self, entry_id: str, data: Dict[str, Any]) -> str:
        """创建单条数据"""
        endpoint = "/app/entry/data/create"
        payload = {
            "app_id": self.app_id,
            "entry_id": entry_id,
            "data": data
        }
        result = self.request('POST', endpoint, payload)
        return result.get('_id')

    def query_data(self, entry_id: str, filters: Dict = None, limit: int = 100) -> List[Dict]:
        """查询数据"""
        endpoint = "/app/entry/data/list"
        payload = {
            "app_id": self.app_id,
            "entry_id": entry_id,
            "limit": limit
        }
        if filters:
            payload["filter"] = filters
        result = self.request('POST', endpoint, payload)
        return result.get('data', [])

    def update_data(self, entry_id: str, data_id: str, data: Dict[str, Any]) -> bool:
        """更新单条数据"""
        endpoint = "/app/entry/data/update"
        payload = {
            "app_id": self.app_id,
            "entry_id": entry_id,
            "data_id": data_id,
            "data": data
        }
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