# stdlib
import logging

# thirdparty
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.task_tracker.services.tasks.api_service import (
    TasksAPI,
    get_tasks_api_service,
)
from src.task_tracker.services.tasks.schemas import TaskInput, Tasks, Users
from src.task_tracker.settings.db import get_session

tasks_router = APIRouter(prefix="/tasks", tags=["Tasks"])
logger = logging.getLogger(__name__)


@tasks_router.get(
    path="",
    description="Get list of tasks",
    response_model=Tasks,
    responses={
        status.HTTP_200_OK: {"description": "List of tasks"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Not Authorized"},
    },
)
async def tasks_list(
    service: TasksAPI = Depends(get_tasks_api_service),
    session: AsyncSession = Depends(get_session),
):
    """
    Get list of tasks
    """
    result = await service.get_tasks_list(session=session)
    return result


@tasks_router.get(
    path="/user-suggestions",
    description="Get list of active users suggestions for create",
    response_model=Users,
    responses={
        status.HTTP_200_OK: {"description": "List of active users"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Not Authorized"},
    },
)
async def active_users_list(
    service: TasksAPI = Depends(get_tasks_api_service),
    session: AsyncSession = Depends(get_session),
):
    """
    Get list of users for suggestions
    """
    result = await service.get_active_users_list(session=session)
    return result


@tasks_router.post(
    path="",
    description="Create task",
    responses={
        status.HTTP_201_CREATED: {"description": "Create task"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Not Authorized"},
    },
)
async def create_task(
    task_input: TaskInput,
    service: TasksAPI = Depends(get_tasks_api_service),
    session: AsyncSession = Depends(get_session),
):
    """
    Get list of tasks
    """
    result = await service.create_task(session=session, task_input=task_input)
    return result
