# Volunteer-Management

基于简道云 API 的轻量化管理后台，专为日常寺庙的义工管理服务。

---

## 项目简介

本系统解决义工管理三大痛点：
- **人员管理**：扫码快速建档，技能标签自动筛选
- **排班签到**：活动→排班→签到数据流自动化
- **工时统计**：实时累加工时，月底一键导出报表

> 当前义工无住宿需求，系统已精简为**3张核心表**，半天可上线。

---

## 技术架构
- **后端**：简道云无代码平台（数据存储、权限管理）
- **自动化**：Python 3.8+（调用官方 OpenAPI）
- **部署**：本地脚本定时执行（无需服务器）

---

## 快速开始（10分钟部署）

### 1. 克隆项目
```bash
git clone https://github.com/your-username/liurong-volunteer.git
cd liurong-volunteer
```

### 2. 配置环境
```bash
# 复制环境模板
cp .env.example .env

# 编辑 .env 文件，填入你的密钥
nano .env
# APP_ID=appXXXXXXXXXXXXX
# API_KEY=sk-XXXXXXXXXXXXX
```
> 密钥获取路径：简道云 → 开放平台 → API Key → 创建并复制

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

### 4. 初始化系统（仅运行一次）
```bash
python scripts/setup_forms.py
```
执行后，简道云后台将自动生成：
- ✅ 义工档案
- ✅ 活动库  
- ✅ 排班签到表
- ✅ 义工实时看板（仪表盘）

---
## 项目结构

```shell
liurong-volunteer/
├── README.md                 # 项目说明（贴仪表盘截图、部署步骤）
├── requirements.txt          # 依赖：requests, python-dotenv
├── .env                      # 密钥配置（gitignore，永不提交）
├── .gitignore               # Python标准 + .env
│
├── config/
│   ├── __init__.py
│   └── settings.py          # 加载.env，定义常量（APP_ID, API_KEY）
│
├── core/
│   ├── __init__.py
│   └── api_client.py        # 唯一与简道云交互的客户端（签名、重试、日志）
│
├── models/
│   ├── __init__.py
│   ├── volunteer.py         # 义工档案模型（增删改查）
│   ├── event.py             # 活动库模型
│   └── schedule.py          # 排班签到模型
│
├── services/
│   ├── __init__.py
│   ├── data_factory.py      # 工时统计、月度积分计算
│   └── notification.py      # 企业微信/公众号模板消息推送
│
├── scripts/
│   ├── __init__.py
│   ├── setup_forms.py       # 初次建表脚本（只跑一次）
│   ├── sync_schedule.py     # 每月1号自动生成排班
│   └── generate_report.py   # 月末导出Excel报表
│
└── tests/
    ├── __init__.py
    └── test_api_client.py   # 测试签名、重试逻辑
```