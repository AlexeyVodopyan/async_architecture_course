# stdlib
import functools

# thirdparty
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.common.schemas.transactions_schemas import (
    ActionType,
    TransactionUpdateMessage,
)
from src.task_tracker.messaging.producers.transaction_producer import (
    TransactionsProducer,
)
from src.task_tracker.services.tasks.queries import (
    get_tasks,
    get_users,
    insert_task,
)
from src.task_tracker.services.tasks.schemas import TaskInput


class TasksAPI:
    def __init__(self):
        self.transactions_producer = TransactionsProducer()

    async def _send_update_to_mq(
        self, action: ActionType, email: str, task_name: str
    ):
        msg = TransactionUpdateMessage(
            action=action, user=email, task_name=task_name
        )
        msg_bytes = self.transactions_producer.prepare_body_message(msg)
        await self.transactions_producer.produce(msg_bytes)

    async def create_task(self, session: AsyncSession, task_input: TaskInput):
        query = insert_task(
            task_input.name, task_input.assigned_to, task_input.description
        )
        await session.execute(query)
        await session.commit()
        await self._send_update_to_mq(
            action=ActionType.ASSIGNED,
            email=task_input.assigned_to,
            task_name=task_input.name,
        )

    async def reassign_tasks(self, session: AsyncSession):
        # TODO: implement shuffle tasks logic in database

        # get all opened tasks

        # then for every task will send message

        # await self._send_update_to_mq(action=ActionType.ASSIGNED,
        #                               email=task_input.assigned_to,
        #                               task_name=task_input.name)
        pass

    @staticmethod
    async def get_tasks_list(
        session: AsyncSession,
    ):
        """
        Get users list
        """
        query = get_tasks()
        results = await session.execute(query)
        return results.mappings().all()

    @staticmethod
    async def get_active_users_list(
        session: AsyncSession,
    ):
        """
        Get users list
        """
        query = get_users()
        results = await session.execute(query)
        return results.mappings().all()


@functools.cache
def get_tasks_api_service() -> TasksAPI:
    return TasksAPI()
