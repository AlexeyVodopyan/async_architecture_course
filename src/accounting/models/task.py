# stdlib
from enum import StrEnum
from uuid import uuid4

# thirdparty
import sqlalchemy
from sqlalchemy import Column, Float, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID

# project
from src.accounting.models.base import Base
from src.accounting.models.mixins import TimeMixin
from src.accounting.models.user import User


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
    closing_price = Column(
        Float,
        comment="Price of closing of this task",
        server_default=sqlalchemy.text("floor(random() * 20 + 20)::int;"),
    )
    assigning_price = Column(
        Float,
        comment="Price of closing of this task",
        server_default=sqlalchemy.text("floor(random() * 10 + 10)::int;"),
    )
    name = Column(String, nullable=False)
    assigned_to = Column(ForeignKey(User.email))
