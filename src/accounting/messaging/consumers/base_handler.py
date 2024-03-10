# stdlib
from abc import ABC, abstractmethod

# thirdparty
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession


class BaseActionHandler(ABC):
    @staticmethod
    @abstractmethod
    async def handle(session: AsyncSession, data: BaseModel):
        pass
