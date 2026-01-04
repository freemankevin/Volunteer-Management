# 职责：封装所有HTTP请求，统一处理签名、超时、重试、日志
import requests
import time
import hashlib
import logging
import json
from typing import Dict, Any, Optional, List
from config.settings import API_KEY, APP_ID

class JDYClient:
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

    def request(self, method: str, endpoint: str, json_data: Optional[Dict] = None, retries: int = 3) -> Dict[str, Any]:
        """发送HTTP请求，带重试机制"""
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
                
                self.logger.info(f"请求: {method} {url} -> {response.status_code}")
                
                if response.status_code == 200:
                    try:
                        result = response.json()
                        if result.get('code') == 0:
                            return result.get('data', {})
                        else:
                            raise Exception(f"API错误: {result.get('msg', '未知错误')} (code: {result.get('code')})")
                    except ValueError as e:
                        # 处理非JSON响应
                        self.logger.error(f"非JSON响应: {response.text[:200]}...")
                        raise Exception(f"响应格式错误: {str(e)}")
                elif response.status_code == 403:
                    raise Exception("权限被拒绝 - 请检查API密钥和APP_ID是否正确")
                else:
                    raise Exception(f"HTTP错误: {response.status_code} - {response.text[:200]}...")
                    
            except Exception as e:
                self.logger.error(f"请求失败 (尝试 {attempt + 1}/{retries}): {str(e)}")
                if attempt == retries - 1:
                    raise
                time.sleep(2 ** attempt)  # 指数退避

    def create_form(self, form_data: Dict[str, Any]) -> str:
        """创建表单
        
        Args:
            form_data: 表单配置数据
            
        Returns:
            表单ID
        """
        endpoint = f"/app/{self.app_id}/entry"
        result = self.request('POST', endpoint, form_data)
        return result.get('entryId')

    def get_form_data(self, entry_id: str, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """获取表单数据
        
        Args:
            entry_id: 表单ID
            limit: 返回记录数量限制
            offset: 偏移量
            
        Returns:
            表单数据列表
        """
        endpoint = f"/app/{self.app_id}/entry/{entry_id}/data"
        params = {"limit": limit, "offset": offset}
        return self.request('GET', endpoint, params)

    def create_form_with_validation(self, form_data: Dict[str, Any]) -> Dict[str, Any]:
        """创建表单并返回完整信息
        
        Args:
            form_data: 表单配置数据
            
        Returns:
            包含表单ID和详细信息的字典
        """
        endpoint = f"/app/{self.app_id}/entry"
        result = self.request('POST', endpoint, form_data)
        return {
            "form_id": result.get('entryId'),
            "form_name": form_data.get('name'),
            "form_url": f"https://www.jiandaoyun.com/f/{result.get('entryId')}",
            "status": "created"
        }

    def create_dashboard(self, dashboard_data: Dict[str, Any]) -> str:
        """创建仪表盘
        
        Args:
            dashboard_data: 仪表盘配置数据
            
        Returns:
            仪表盘ID
        """
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

    def update_form(self, entry_id: str, form_data: Dict[str, Any]) -> bool:
        """更新表单"""
        endpoint = f"/app/{self.app_id}/entry/{entry_id}"
        self.request('PUT', endpoint, form_data)
        return True

    def delete_form(self, entry_id: str) -> bool:
        """删除表单"""
        endpoint = f"/app/{self.app_id}/entry/{entry_id}"
        self.request('DELETE', endpoint)
        return True