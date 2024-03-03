# stdlib
from enum import StrEnum

# thirdparty
from pydantic import BaseModel


class ActionType(StrEnum):
    ASSIGNED = "assigned"
    CLOSED = "closed"


class TransactionUpdateMessage(BaseModel):
    action: ActionType
    user: str
    task_name: str
