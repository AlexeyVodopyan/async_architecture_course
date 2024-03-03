# stdlib
from enum import StrEnum

# thirdparty
from pydantic import BaseModel


class Role(StrEnum):
    PARROT = "parrot"
    MANAGER = "manager"
    ACCOUNTANT = "accountant"


class ActionType(StrEnum):
    created = "CREATED"
    updated = "UPDATED"


class UserData(BaseModel):
    email: str
    role: Role
    is_active: bool
    first_name: str | None = None
    last_name: str | None = None


class UserUpdateMessage(BaseModel):
    action: ActionType
    data: UserData
