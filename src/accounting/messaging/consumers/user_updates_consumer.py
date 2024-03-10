# stdlib
import logging
import typing

# project
from src.accounting.messaging.consumers.action_handlers import (
    CreatedActionHandler,
    UpdatedActionHandler,
)
from src.accounting.settings.config import settings
from src.accounting.settings.db import get_session_cm
from src.common.messaging.consumers.rabbit_base_consumer import (
    RabbitConsumerFabric,
)
from src.common.schemas.v1.user_updates_schemas import (
    UserActionType as ActionType,
)
from src.common.schemas.v1.user_updates_schemas import (
    UserUpdateMessageV1 as UserUpdateMessage,
)

logger = logging.getLogger(__name__)


class UsersUpdatesConsumer(RabbitConsumerFabric):
    def __init__(self, prefetch_count=1):
        super().__init__(prefetch_count)
        self.action_strategy = {
            ActionType.created: CreatedActionHandler(),
            ActionType.updated: UpdatedActionHandler(),
        }

    @property
    def connection_kwargs(self):
        return {
            "host": settings.mq.host,
            "port": settings.mq.port,
            "login": settings.mq.user,
            "password": settings.mq.password,
        }

    @property
    def exchange(self) -> str:
        return settings.mq.user_updates_exchange

    @property
    def queues(self) -> list[str]:
        return [settings.mq.user_updates_exchange]

    @property
    def msg_model(self) -> typing.Type[UserUpdateMessage]:
        """Message data model type"""
        return UserUpdateMessage

    def set_strategy(self, action: ActionType):
        handler = self.action_strategy.get(action)

        if not handler:
            logger.error(
                "Action handler is not provided for this type of message"
            )
            raise NotImplementedError
        return handler

    async def main_action(self, msg: UserUpdateMessage, *args, **kwargs):
        """Main action for saving of preprocessing results"""

        try:
            handler = self.set_strategy(msg.action)
        except NotImplementedError:
            return

        async with get_session_cm() as session:
            await handler.handle(session, user_data=msg.data)

        logger.info("User information was saved to database")
