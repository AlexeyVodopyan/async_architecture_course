# stdlib
import uuid

# thirdparty
from pydantic import BaseModel, ConfigDict, RootModel

# project
from src.task_tracker.models import TaskStatus


class Task(BaseModel):
    id: uuid.UUID
    name: str
    description: str | None
    assigned_to: str
    first_name: str | None
    last_name: str | None
    status: TaskStatus

    model_config = ConfigDict(from_attributes=True)


class Tasks(RootModel):
    root: list[Task]


class User(BaseModel):
    first_name: str | None
    last_name: str | None
    email: str


class Users(RootModel):
    root: list[User]
    model_config = ConfigDict(from_attributes=True)


class TaskInput(BaseModel):
    name: str
    assigned_to: str
    description: str | None
