# 寺院义工管理系统设置指南

## 🚨 当前问题：HTTP 403错误

你遇到的HTTP 403错误表示权限被拒绝，这通常是由于以下原因之一：

## 🔍 问题排查步骤

### 1. 验证API配置

运行调试工具：
```bash
python3 debug_api.py
```

### 2. 检查API密钥和APP_ID

#### 获取正确的API密钥：
1. 登录简道云官网：https://www.jiandaoyun.com
2. 进入 **账户设置** → **API密钥**
3. 创建新的API密钥或确认现有密钥有效

#### 获取正确的APP_ID：
1. 进入你的目标应用
2. 查看浏览器URL：`https://www.jiandaoyun.com/app/XXXXXX`
3. `XXXXXX`就是你的APP_ID

### 3. 检查权限设置

#### 确保API密钥有权限：
- 访问目标应用
- 创建表单和仪表盘
- 没有IP白名单限制

#### 检查应用权限：
- 确认应用没有设置为私有
- 确认你有管理员权限

### 4. 更新配置文件

编辑 `.env` 文件：
```bash
# 简道云API配置
JDY_API_KEY=你的正确API密钥
JDY_APP_ID=你的正确应用ID

# 日志配置
LOG_LEVEL=INFO
```

## 🧪 测试连接

### 基础测试：
```python
import requests
import hashlib
import time

API_KEY = "你的API密钥"
APP_ID = "你的应用ID"

timestamp = str(int(time.time() * 1000))
sign_str = f'{API_KEY}{timestamp}'
signature = hashlib.md5(sign_str.encode('utf-8')).hexdigest()

headers = {
    'Content-Type': 'application/json',
    'X-Api-Key': API_KEY,
    'X-Timestamp': timestamp,
    'X-Sign': signature
}

# 测试获取应用信息
url = f"https://api.jiandaoyun.com/api/v2/app/{APP_ID}/entry"
response = requests.get(url, headers=headers)
print(f"状态码: {response.status_code}")
print(f"响应: {response.text[:200]}")
```

## 📋 常见问题解决

### 问题1：403 Forbidden
**可能原因**：
- API密钥无效
- APP_ID错误
- 没有访问权限
- IP地址限制

**解决方案**：
1. 重新生成API密钥
2. 确认APP_ID正确
3. 检查应用权限设置
4. 联系简道云客服

### 问题2：401 Unauthorized
**可能原因**：
- 签名错误
- 时间戳过期
- 密钥格式错误

**解决方案**：
1. 检查签名生成逻辑
2. 确保时间戳是当前时间
3. 确认密钥格式正确

### 问题3：404 Not Found
**可能原因**：
- APP_ID不存在
- 端点URL错误

**解决方案**：
1. 确认APP_ID存在
2. 检查API端点URL

## 🔧 快速验证

### 1. 检查API密钥有效性：
```bash
curl -X GET \
  "https://api.jiandaoyun.com/api/v2/app/你的APP_ID/entry" \
  -H "X-Api-Key: 你的API密钥"
```

### 2. 检查应用权限：
登录简道云后台，确认：
- 应用存在且可访问
- API密钥有创建表单权限
- 没有IP白名单限制

## 📞 联系支持

如果以上步骤都无法解决问题：

1. **简道云客服**：400-111-0909
2. **在线客服**：官网右下角在线客服
3. **技术文档**：https://docs.jiandaoyun.com

## ✅ 验证成功标志

当配置正确时，你应该看到：
- 状态码200
- JSON格式的响应数据
- 包含应用信息或表单列表

运行调试工具确认：
```bash
python3 debug_api.py
```