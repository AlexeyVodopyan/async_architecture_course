# stdlib
import logging

# thirdparty
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.accounting.messaging.consumers.base_handler import BaseActionHandler
from src.accounting.models.user import User
from src.common.schemas.v1.user_updates_schemas import (
    UserUpdateEventData as UserData,
)

logger = logging.getLogger(__name__)


class UpdatedActionHandler(BaseActionHandler):
    @staticmethod
    async def handle(session: AsyncSession, data: UserData):
        query = (
            update(User)
            .filter(User.email == data.email)
            .values(data.model_dump())
        )
        await session.execute(query)
        await session.commit()
