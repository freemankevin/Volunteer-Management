# 职责：项目第一次运行时，调用 models 下的三个类方法，一次性建三张表
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.volunteer import VolunteerModel
from models.event import EventModel
from models.schedule import ScheduleModel

if __name__ == "__main__":
    VolunteerModel.create_form()
    EventModel.create_form()
    ScheduleModel.create_form()