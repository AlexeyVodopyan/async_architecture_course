# stdlib
from datetime import datetime
from uuid import UUID

# thirdparty
from pydantic import BaseModel


class TaskWorkFlowData(BaseModel):
    user_assigned_to: str
    task_name: str


class TaskWorkFlowMessageV1(BaseModel):
    """TaskWorkFlow schema v1"""

    data: TaskWorkFlowData
    version: str = "1"
    event_id: UUID
    event_time: datetime = datetime.now()
