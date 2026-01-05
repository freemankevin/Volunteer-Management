# 义工管理系统

基于简道云 API 的轻量化义工管理后台。

> ⚠️ **重要说明**：
> 1. 简道云 API 不支持创建表单，需要先在简道云后台手动创建表单，然后通过 API 操作数据。
> 2. 只有试用版、企业版+ 才能使用 API 操作表单数据，免费版、标准版本无法使用。


## 🚀 快速开始

### 步骤 1：准备环境

```bash
# 克隆项目
git clone <repo-url>
cd volunteer-management

# 安装依赖
pip install -r requirements.txt
```

### 步骤 2：获取 API 密钥

1. 登录 https://www.jiandaoyun.com
2. 点击右上角头像 → **开放平台** → **密钥管理**
3. 创建新 API 密钥，复制保存

### 步骤 3：创建表单

**这是最重要的一步！**

1. 阅读 [表单创建指南](docs/表单创建指南.md)
2. 在简道云后台手动创建 3 个表单：
   - 义工档案表
   - 活动库表
   - 排班签到表
3. 获取每个表单的 ENTRY_ID

### 步骤 4：配置环境变量

复制 `.env.example` 为 `.env`：

```bash
cp .env.example .env
```

编辑 `.env` 文件，填入你的配置：

```env
# 简道云API配置
JDY_API_KEY=你的API密钥
JDY_APP_ID=你的应用ID

# 表单ID配置（从步骤3获取）
JDY_VOLUNTEER_ENTRY_ID=义工档案表的ENTRY_ID
JDY_EVENT_ENTRY_ID=活动库表的ENTRY_ID
JDY_SCHEDULE_ENTRY_ID=排班签到表的ENTRY_ID

# 日志配置
LOG_LEVEL=INFO
```

### 步骤 5：验证配置

```bash
python scripts/init_system.py
```

预期输出：

```
🔧 简道云表单配置验证
============================================================
✅ API_KEY: osVkYmjz...
✅ APP_ID: 6959dd6d1a3803d498daa91b

📋 验证表单配置...
✅ 义工档案表 (ENTRY_ID: xxx) - 找到 6 个字段
✅ 活动库表 (ENTRY_ID: xxx) - 找到 8 个字段
✅ 排班签到表 (ENTRY_ID: xxx) - 找到 8 个字段

🎉 所有表单配置正确！可以开始使用系统了。
```

---

## 📁 项目结构

```
volunteer-management/
├── config/          # 配置管理
│   └── settings.py  # 环境变量加载
├── core/            # API客户端（核心）
│   └── api_client.py
├── models/          # 数据模型（义工/活动/排班）
│   ├── volunteer.py
│   ├── event.py
│   └── schedule.py
├── scripts/         # 工具脚本
│   └─init_system.─ py  # 表单验证脚本
├── requirements.txt # 依赖
├── .env.example     # 配置模板
└── README.md        # 本文件
```

---

## 🔧 常见问题

### Q1: 为什么不能通过 API 创建表单？

简道云是零代码平台，表单创建是通过可视化界面完成的。API 主要用于数据操作（增删改查），不支持创建表单结构。

### Q2: 403 权限被拒绝

- 检查 `.env` 中 API_KEY 是否正确
- 确保 API 密钥有数据操作权限
- 重新生成 API 密钥试试

### Q3: 404 找不到表单

- 检查 ENTRY_ID 是否正确
- 确保在简道云后台已创建对应的表单
- 参考 [表单创建指南](docs/表单创建指南.md)

### Q4: 找不到模块

```bash
# 确保安装了依赖
pip install -r requirements.txt

# 在项目目录运行脚本
cd /path/to/volunteer-management
python scripts/init_system.py
```

### Q5: 如何获取 ENTRY_ID？

1. 在简道云后台打开表单
2. 点击"编辑"按钮
3. 查看浏览器地址栏：
   ```
   https://www.jiandaoyun.com/app/{APP_ID}/form/{ENTRY_ID}
                                                  ↑
                                            这就是 ENTRY_ID
   ```

---

## 📖 API 文档

- [简道云官方文档](https://hc.jiandaoyun.com/doc/12596)
- [简道云 API 文档](https://hc.jiandaoyun.com/open/10992)
- [表单和数据接口](https://hc.jiandaoyun.com/open/10993)
- [简道云 Openapi 多语言调用示例](https://github.com/heyjackgo/jdy-api/tree/master)