# core/api_client.py - 精简版本（只保留必要的）
import requests
import time
import hashlib
import logging
from typing import Dict, Any, Optional, List
from config.settings import API_KEY, APP_ID

class JDYClient:
    """简道云API客户端 - 核心版本"""
    
    def __init__(self):
        self.base_url = "https://api.jiandaoyun.com/api/v5"
        self.app_id = APP_ID
        self.api_key = API_KEY
        self.logger = logging.getLogger("JDYClient")
    
    def _make_auth_headers(self) -> Dict[str, str]:
        """生成认证头部"""
        timestamp = str(int(time.time() * 1000))
        sign_str = f'{self.api_key}{timestamp}'
        signature = hashlib.md5(sign_str.encode('utf-8')).hexdigest()
        
        return {
            'Content-Type': 'application/json',
            'X-Api-Key': self.api_key,
            'X-Timestamp': timestamp,
            'X-Sign': signature
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
                    result = response.json()
                    if result.get('code') == 0:
                        return result.get('data', {})
                    else:
                        raise Exception(f"API error: {result.get('msg')}")
                elif response.status_code == 403:
                    raise Exception("权限被拒绝 - 检查API密钥")
                else:
                    raise Exception(f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.logger.error(f"请求失败 (尝试 {attempt + 1}/{retries}): {str(e)}")
                if attempt == retries - 1:
                    raise
                time.sleep(2 ** attempt)

    def create_form(self, form_data: Dict[str, Any]) -> str:
        """创建表单"""
        endpoint = f"/app/{self.app_id}/entry"
        result = self.request('POST', endpoint, form_data)
        return result.get('entryId')

    def create_dashboard(self, dashboard_data: Dict[str, Any]) -> str:
        """创建仪表盘"""
        endpoint = f"/app/{self.app_id}/dashboard"
        result = self.request('POST', endpoint, dashboard_data)
        return result.get('dashboardId')

    def get_form_list(self) -> List[Dict[str, Any]]:
        """获取表单列表"""
        endpoint = f"/app/{self.app_id}/form"
        return self.request('GET', endpoint)

    def get_dashboard_list(self) -> List[Dict[str, Any]]:
        """获取仪表盘列表"""
        endpoint = f"/app/{self.app_id}/dashboard"
        return self.request('GET', endpoint)