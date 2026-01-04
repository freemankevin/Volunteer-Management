# 职责：加载环境变量，校验必填项
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("JDY_API_KEY")
APP_ID = os.getenv("JDY_APP_ID")

VOLUNTEER_ENTRY_ID = os.getenv("JDY_VOLUNTEER_ENTRY_ID")
EVENT_ENTRY_ID = os.getenv("JDY_EVENT_ENTRY_ID")
SCHEDULE_ENTRY_ID = os.getenv("JDY_SCHEDULE_ENTRY_ID")

assert API_KEY and APP_ID, "请先配置 .env 文件中的 JDY_API_KEY 和 JDY_APP_ID"