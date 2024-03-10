# stdlib
import logging
import typing

# project
from src.accounting.messaging.consumers.task_workflow_handlers.task_assigned_handler import (
    TaskAssignedHandler,
)
from src.accounting.settings.config import settings
from src.accounting.settings.db import get_session_cm
from src.common.messaging.consumers.rabbit_base_consumer import (
    RabbitConsumerFabric,
)
from src.common.schemas.v1.task_workflow_schemas import TaskWorkFlowMessageV1

logger = logging.getLogger(__name__)


class TaskAssignedConsumer(RabbitConsumerFabric):
    def __init__(self, prefetch_count=1):
        super().__init__(prefetch_count)
        self.handler = TaskAssignedHandler()

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
        return [settings.mq.user_updates_queue]

    @property
    def msg_model(self) -> typing.Type[TaskWorkFlowMessageV1]:
        """Message data model type"""
        return TaskWorkFlowMessageV1

    async def main_action(self, msg: TaskWorkFlowMessageV1, *args, **kwargs):
        """Main action for saving of preprocessing results"""

        async with get_session_cm() as session:
            await self.handler.handle(session, data=msg.data)

        logger.info("Task information was updated to database")
