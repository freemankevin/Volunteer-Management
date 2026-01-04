# 义工管理系统

基于简道云 API 的轻量化义工管理后台。

## 🚀 5分钟快速开始

### 1. 准备环境

```bash
# 克隆项目
git clone <repo-url>
cd volunteer-management

# 安装依赖
pip install -r requirements.txt

# 配置API密钥
cp .env.example .env
nano .env  # 填入 JDY_API_KEY 和 JDY_APP_ID
```

### 2. 获取API密钥

1. 登录 https://www.jiandaoyun.com
2. 点击右上角 **账户设置** → **API密钥**
3. 创建新API密钥，复制粘贴到 `.env` 文件

APP_ID 在应用URL中：`https://www.jiandaoyun.com/app/APP_ID`

### 3. 验证配置

```bash
python quick_check.py
```

预期输出：
```
✅ API_KEY: sk-XXXX...
✅ APP_ID: appXXXX
✅ core.api_client
✅ API连接成功，找到 X 个表单
🎉 所有检查通过！
```

### 4. 初始化系统

```bash
python scripts/init_system.py
```

预期输出：
```
✅ 义工档案表单: entryXXXX
✅ 活动库表单: entryXXXX
✅ 排班签到表单: entryXXXX
🎉 系统初始化完成！
```

## 📁 项目结构

```
volunteer-management/
├── config/          # 配置管理
├── core/            # API客户端（核心）
├── models/          # 数据模型（义工/活动/排班）
├── scripts/         # 初始化脚本
├── requirements.txt # 依赖
├── .env.example     # 配置模板
└── README.md        # 本文件
```

## 💻 基础使用

### 创建义工

```python
from models.volunteer import VolunteerModel

VolunteerModel.create(
    name="张三",
    phone="13800138000",
    age=35,
    skills="医疗、摄影"
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
    location="大雄宝殿"
)
```

### 排班签到

```python
from models.schedule import ScheduleModel

# 创建排班
ScheduleModel.create(
    volunteer_name="张三",
    event_name="春节祈福法会",
    event_date="2024-02-10",
    role="接待员"
)

# 签到
ScheduleModel.check_in(record_id)

# 签退（指定工时）
ScheduleModel.check_out(record_id, 8.0)
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

## 🔧 常见问题

### Q1: 403 权限被拒绝
- 检查 `.env` 中 API_KEY 和 APP_ID 是否正确
- 确保API密钥有创建表单权限
- 重新生成API密钥试试

### Q2: 找不到模块
```bash
# 确保安装了依赖
pip install -r requirements.txt

# 在项目目录运行脚本
cd /path/to/volunteer-management
python quick_check.py
```

### Q3: 如何创建自定义表单
编辑 `scripts/init_system.py` 中的 `create_forms()` 函数，修改 `widgets` 配置。

## 📖 API文档

详见 [简道云官方文档](https://docs.jiandaoyun.com)

## 📝 数据字段说明

### 义工档案表（VolunteerModel）
- `name` - 义工姓名
- `phone` - 手机号
- `age` - 年龄（16-80）
- `gender` - 性别（男/女）
- `skills` - 技能特长
- `status` - 状态（活跃/暂停/退出）

### 活动库表（EventModel）
- `event_name` - 活动名称
- `event_date` - 活动日期
- `start_time` - 开始时间
- `end_time` - 结束时间
- `location` - 活动地点
- `status` - 活动状态

### 排班签到表（ScheduleModel）
- `volunteer_name` - 义工姓名
- `event_name` - 活动名称
- `event_date` - 活动日期
- `role` - 担任角色
- `status` - 签到状态
- `hours` - 工时

## 🛠️ 开发指南

### 添加新表单字段

在 `scripts/init_system.py` 的表单定义中添加：

```python
{
    "type": "text",           # 字段类型
    "name": "field_name",     # 字段名
    "label": "字段标签",       # 显示标签
    "required": True,         # 是否必填
}
```

支持的字段类型：
- `text` - 文本
- `phone` - 电话
- `email` - 邮箱
- `number` - 数字
- `date` - 日期
- `time` - 时间
- `select` - 下拉选择
- `textarea` - 多行文本

### 扩展API客户端

在 `core/api_client.py` 中添加新方法：

```python
def custom_method(self, ...):
    """自定义方法"""
    endpoint = f"/app/{self.app_id}/custom"
    return self.request('GET', endpoint, ...)
```

## 📞 技术支持

- 简道云官方：https://www.jiandaoyun.com
- 文档：https://docs.jiandaoyun.com
- 联系：400-111-0909

## 📄 License

MIT