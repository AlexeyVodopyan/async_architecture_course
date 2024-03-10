# stdlib
import logging

# thirdparty
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.accounting.messaging.consumers.base_handler import BaseActionHandler
from src.accounting.models import (
    BillingCycle,
    BillingCycleStatus,
    Task,
    Transaction,
)
from src.common.schemas.v1.task_workflow_schemas import TaskWorkFlowData

logger = logging.getLogger(__name__)


class TaskAssignedHandler(BaseActionHandler):
    @staticmethod
    async def handle(session: AsyncSession, data: TaskWorkFlowData):

        query = (
            update(Task)
            .filter(Task.public_id == data.task_public_id)
            .values(assigned_to=data.user_assigned_to, name=data.task_name)
            .returning(Task.assigning_price, Task.id)
        )
        result = await session.execute(query)
        result = result.all()

        # insert transaction to open billing cycle
        if result:
            # open billing cycle id
            query = select(BillingCycle.id).filter(
                BillingCycle.user == data.user_assigned_to,
                BillingCycle.status == BillingCycleStatus.open,
            )

            billing_cycle_id = await session.execute(query)
            billing_cycle_id = billing_cycle_id.scalar()

            query = insert(Transaction).values(
                task_id=result[0][1],
                description=data.task_name,
                value=-result[0][0],
                billing_cycle_id=billing_cycle_id,
            )
            await session.execute(query)
            await session.commit()
        else:
            logger.info(f"Task with id = {data.task_public_id} not found")
