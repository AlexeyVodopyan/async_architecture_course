# stdlib
import functools
import uuid

# thirdparty
from fastapi import status
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.common.schemas.error import ExceptionBody, HTTPException
from src.common.schemas.transactions_schemas import (
    ActionType,
    TransactionUpdateMessage,
)
from src.task_tracker.messaging.producers.transaction_producer import (
    TransactionsProducer,
)
from src.task_tracker.services.tasks.queries import (
    close_task,
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

    async def close_task(self, session: AsyncSession, task_id: uuid.UUID):
        query = close_task(task_id)
        results = await session.execute(query)
        task_info = results.all()

        if task_info:
            await session.commit()
            await self._send_update_to_mq(
                action=ActionType.CLOSED,
                email=task_info[0][1],
                task_name=task_info[0][0],
            )
            return

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ExceptionBody(
                [
                    {
                        "message": "Task is not found, check request params",
                        "error": "BAD_REQUEST",
                    }
                ]
            ),
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
