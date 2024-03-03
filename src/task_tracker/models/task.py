# stdlib
from enum import StrEnum
from uuid import uuid4

# thirdparty
import sqlalchemy
from sqlalchemy import Column
from sqlalchemy import Enum as SAEnum
from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

# project
from src.task_tracker.models.base import Base
from src.task_tracker.models.mixins import TimeMixin
from src.task_tracker.models.user import User


class TaskStatus(StrEnum):
    OPEN = "open"
    CLOSED = "closed"


class Task(Base, TimeMixin):
    __tablename__ = "task"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        comment="ID",
        default=uuid4,
        server_default=sqlalchemy.text("gen_random_uuid()"),
    )
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    status = Column(SAEnum(TaskStatus, name="task_status"), nullable=False)
    assigned_to = Column(ForeignKey(User.email))
