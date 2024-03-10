# stdlib
from datetime import datetime
from enum import StrEnum
from uuid import UUID

# thirdparty
from pydantic import BaseModel


class Role(StrEnum):
    PARROT = "parrot"
    MANAGER = "manager"
    ACCOUNTANT = "accountant"


class UserActionType(StrEnum):
    created = "user_created"
    updated = "user_updated"


class UserUpdateEventData(BaseModel):
    email: str
    role: Role
    is_active: bool
    first_name: str | None = None
    last_name: str | None = None


class UserUpdateMessageV1(BaseModel):
    """User update schema v1"""

    action: UserActionType
    data: UserUpdateEventData
    version: str = "1"
    event_id: UUID
    event_time: datetime = datetime.now()
