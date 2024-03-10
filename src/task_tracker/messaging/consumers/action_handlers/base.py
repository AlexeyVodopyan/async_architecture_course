# stdlib
from abc import ABC, abstractmethod

# thirdparty
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.common.schemas.v1.user_updates_schemas import (
    UserUpdateEventData as UserData,
)


class BaseActionHandler(ABC):
    @staticmethod
    @abstractmethod
    async def handle(session: AsyncSession, user_data: UserData):
        pass
