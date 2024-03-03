# stdlib
import logging

# thirdparty
from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.common.schemas.user_updates_schemas import UserData
from src.task_tracker.messaging.consumers.action_handlers.base import (
    BaseActionHandler,
)
from src.task_tracker.models.user import User

logger = logging.getLogger(__name__)


class UpdatedActionHandler(BaseActionHandler):
    @staticmethod
    async def handle(session: AsyncSession, user_data: UserData):
        query = (
            update(User)
            .filter(User.email == user_data.email)
            .values(user_data.model_dump())
        )
        await session.execute(query)
        await session.commit()
