# 义工管理系统

基于简道云 API 的轻量化义工管理后台。

> ⚠️ **重要说明**：简道云 API 不支持创建表单，需要先在简道云后台手动创建表单，然后通过 API 操作数据。

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
├── docs/            # 文档
│   └── 表单创建指南.md
├── requirements.txt # 依赖
├── .env.example     # 配置模板
└── README.md        # 本文件
```

---

## 💻 基础使用

### 创建义工

```python
from models.volunteer import VolunteerModel

VolunteerModel.create(
    name="张三",
    phone="13800138000",
    age=35,
    gender="男",
    skills="医疗、摄影",
    status="活跃"
)
```

### 创建活动

```python
from models.event import EventModel

EventModel.create(
    event_name="春节祈福法会",
    event_date="2024-02-10",
    start_time="09:00",
    end_time="17:00",
    location="大雄宝殿",
    volunteers_needed=20,
    status="计划中"
)
```

### 排班签到

```python
from models.schedule import ScheduleModel

# 创建排班
schedule_id = ScheduleModel.create(
    volunteer_name="张三",
    volunteer_phone="13800138000",
    event_name="春节祈福法会",
    event_date="2024-02-10",
    role="接待员",
    status="已排班"
)

# 签到
ScheduleModel.check_in(schedule_id)

# 签退（记录工时）
ScheduleModel.check_out(schedule_id, hours=8.0)
```

### 数据查询

```python
# 获取所有义工
volunteers = VolunteerModel.list_all()

# 按状态筛选
active = VolunteerModel.list_by_status("活跃")

# 按名字搜索
found = VolunteerModel.search_by_name("张三")

# 义工工时统计
hours = ScheduleModel.get_volunteer_hours("张三")
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

---

## 📝 数据字段说明

### 义工档案表（VolunteerModel）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| name | 文本 | ✅ | 义工姓名 |
| phone | 文本 | ✅ | 手机号码 |
| age | 数字 | ✅ | 年龄（16-80） |
| gender | 下拉框 | ✅ | 性别（男/女） |
| skills | 多行文本 | ❌ | 技能特长 |
| status | 下拉框 | ✅ | 状态（活跃/暂停/退出） |

### 活动库表（EventModel）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| event_name | 文本 | ✅ | 活动名称 |
| event_date | 日期 | ✅ | 活动日期 |
| start_time | 时间 | ✅ | 开始时间 |
| end_time | 时间 | ✅ | 结束时间 |
| location | 文本 | ✅ | 活动地点 |
| volunteers_needed | 数字 | ❌ | 需要人数 |
| status | 下拉框 | ✅ | 活动状态 |

### 排班签到表（ScheduleModel）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| volunteer_name | 文本 | ✅ | 义工姓名 |
| volunteer_phone | 文本 | ✅ | 义工电话 |
| event_name | 文本 | ✅ | 活动名称 |
| event_date | 日期 | ✅ | 活动日期 |
| role | 下拉框 | ❌ | 担任角色 |
| status | 下拉框 | ✅ | 签到状态 |
| hours | 数字 | ❌ | 工时 |

---

## 🛠️ 开发指南

### 扩展 API 客户端

在 `core/api_client.py` 中添加新方法：

```python
def custom_query(self, entry_id: str, custom_filter: Dict):
    """自定义查询"""
    endpoint = f"/app/{self.app_id}/entry/{entry_id}/data"
    payload = {"filter": custom_filter, "limit": 100}
    return self.request('POST', endpoint, payload)
```

### 添加新的数据模型

参考 `models/volunteer.py` 创建新模型：

```python
from core.api_client import JDYClient
from config.settings import YOUR_ENTRY_ID

class YourModel:
    client = JDYClient()
    entry_id = YOUR_ENTRY_ID
    
    @classmethod
    def create(cls, **data):
        return cls.client.create_data(cls.entry_id, data)
```

---

## 📄 许可证

MIT License

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！