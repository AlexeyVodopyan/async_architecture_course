# thirdparty
from sqlalchemy import Column, DateTime, func
from sqlalchemy.orm import declared_attr


class TimeMixin:
    @declared_attr
    def created_at(cls):
        return Column(
            DateTime,
            server_default=func.now(),
            nullable=False,
            comment="Creation date",
        )

    @declared_attr
    def modified_at(cls):
        return Column(
            DateTime,
            server_default=func.now(),
            nullable=False,
            comment="Modified date",
        )
