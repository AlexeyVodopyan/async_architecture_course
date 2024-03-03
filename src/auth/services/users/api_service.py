# stdlib
import functools
import logging

# thirdparty
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.auth.messaging.producers.user_updates_producer import (
    UsersUpdatesProducer,
)
from src.auth.models.user import Role
from src.auth.services.users.queries import get_users, update_user_data
from src.common.schemas.user_updates_schemas import (
    ActionType,
    UserData,
    UserUpdateMessage,
)

logger = logging.getLogger(__name__)


class UsersAPI:
    def __init__(self):
        self.user_updates_producer = UsersUpdatesProducer()

    async def _send_update_to_mq(
        self,
        action: ActionType,
        email: str,
        role: Role,
        first_name: str,
        last_name: str,
        is_active: bool,
    ):
        msg = UserUpdateMessage(
            action=action,
            data=UserData(
                email=email,
                role=role,
                is_active=is_active,
                first_name=first_name,
                last_name=last_name,
            ),
        )
        msg_bytes = self.user_updates_producer.prepare_body_message(msg)
        await self.user_updates_producer.produce(msg_bytes)

    @staticmethod
    async def get_users_list(
        session: AsyncSession,
    ):
        """
        Get users list
        """
        query = get_users()
        results = await session.execute(query)
        return results.mappings().all()

    async def update_user_info(
        self, session: AsyncSession, email: str, user_data: UserData
    ):
        """
        Get users list
        """
        query = update_user_data(email, user_data)
        await session.execute(query)
        await session.commit()

        await self._send_update_to_mq(
            ActionType.updated,
            email,
            user_data.role,
            user_data.first_name,
            user_data.last_name,
            user_data.is_active,
        )


@functools.cache
def get_users_api_service() -> UsersAPI:
    return UsersAPI()
