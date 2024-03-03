# thirdparty
from sqlalchemy import Boolean, Column
from sqlalchemy import Enum as SAEnum
from sqlalchemy import String
from sqlalchemy_utils import PasswordType

# project
from src.auth.models.base import Base
from src.auth.models.mixins import TimeMixin
from src.common.schemas.user_updates_schemas import Role


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

    password = Column(
        PasswordType(
            schemes=["pbkdf2_sha512", "md5_crypt"], deprecated=["md5_crypt"]
        ),
        nullable=False,
    )
    role = Column(SAEnum(Role), comment="User Role", nullable=False)
