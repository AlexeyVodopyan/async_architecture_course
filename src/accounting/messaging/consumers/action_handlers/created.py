# stdlib
import logging

# thirdparty
from sqlalchemy import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.accounting.messaging.consumers.action_handlers.base import (
    BaseActionHandler,
)
from src.accounting.models.user import User
from src.common.schemas.v1.user_updates_schemas import (
    UserUpdateEventData as UserData,
)

logger = logging.getLogger(__name__)


class CreatedActionHandler(BaseActionHandler):
    @staticmethod
    async def handle(session: AsyncSession, user_data: UserData):
        query = insert(User).values(user_data.model_dump())
        try:
            await session.execute(query)
            await session.commit()

        except IntegrityError as e:
            logger.error(e)
