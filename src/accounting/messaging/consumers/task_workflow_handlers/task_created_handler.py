# stdlib
import logging
import uuid

# thirdparty
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.accounting.messaging.consumers.base_handler import BaseActionHandler
from src.accounting.models.task import Task
from src.common.schemas.v1.task_workflow_schemas import TaskWorkFlowData

logger = logging.getLogger(__name__)


class TaskCreatedHandler(BaseActionHandler):
    @staticmethod
    async def handle(session: AsyncSession, data: TaskWorkFlowData):

        query = insert(Task).values(
            id=uuid.uuid4(),
            public_id=data.task_public_id,
            assigned_to=data.user_assigned_to,
            name=data.task_name,
        )
        await session.execute(query)
        await session.commit()
