# stdlib
import functools

# thirdparty
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.task_tracker.services.tasks.queries import (
    get_tasks,
    get_users,
    insert_task,
)
from src.task_tracker.services.tasks.schemas import TaskInput


class TasksAPI:
    # def __init__(self):
    # self.tranactions_producer = UsersUpdatesProducer()

    # async def _send_update_to_mq(
    #     self,
    #     action: ActionType,
    #     email: str,
    #     role: Role,
    #     first_name: str,
    #     last_name: str,
    #     is_active: bool,
    # ):
    #     msg = UserUpdateMessage(
    #         action=action,
    #         data=UserData(
    #             email=email,
    #             role=role,
    #             is_active=is_active,
    #             first_name=first_name,
    #             last_name=last_name,
    #         ),
    #     )
    #     msg_bytes = self.user_updates_producer.prepare_body_message(msg)
    #     await self.user_updates_producer.produce(msg_bytes)

    @staticmethod
    async def create_task(session: AsyncSession, task_input: TaskInput):
        query = insert_task(
            task_input.name, task_input.assigned_to, task_input.description
        )
        await session.execute(query)
        await session.commit()

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
