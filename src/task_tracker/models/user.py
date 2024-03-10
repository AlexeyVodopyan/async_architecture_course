# thirdparty
from sqlalchemy import Boolean, Column
from sqlalchemy import Enum as SAEnum
from sqlalchemy import String

# project
from src.common.schemas.v1.user_updates_schemas import Role
from src.task_tracker.models.base import Base
from src.task_tracker.models.mixins import TimeMixin


class User(TimeMixin, Base):
    """Table for storing users info"""

    __tablename__ = "user"

    email = Column(
        String,
        comment="Email of user",
        primary_key=True,
    )
    first_name = Column(
        String,
        comment="First Name of user",
        nullable=True,
    )
    last_name = Column(
        String,
        comment="Last Name of user",
        nullable=True,
    )

    is_active = Column(
        Boolean,
        nullable=False,
        default=True,
        comment="Is this user active or not",
    )
    role = Column(SAEnum(Role), comment="User Role", nullable=False)
