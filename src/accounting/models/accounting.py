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
from src.accounting.models.base import Base
from src.accounting.models.mixins import TimeMixin
from src.accounting.models.task import Task
from src.accounting.models.user import User


class BillingCycleStatus(StrEnum):
    open = "open"
    paid = "paid"


class BillingCycle(TimeMixin, Base):
    """Table for billing cycles for users"""

    __tablename__ = "billing_cycle"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        comment="ID",
        default=uuid4,
        server_default=sqlalchemy.text("gen_random_uuid()"),
    )

    user = Column(ForeignKey(User.email))
    status = Column(
        SAEnum(BillingCycleStatus), comment="Billing Cycle", nullable=False
    )


class Transaction(TimeMixin, Base):
    """Table for single transaction"""

    __tablename__ = "transaction"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        comment="ID",
        default=uuid4,
        server_default=sqlalchemy.text("gen_random_uuid()"),
    )

    billing_cycle_id = Column(ForeignKey(BillingCycle.id))
    description = Column(String, comment="Description of transaction")
    task_id = Column(ForeignKey(Task.id))
