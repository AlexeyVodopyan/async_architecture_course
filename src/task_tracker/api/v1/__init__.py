# thirdparty
from fastapi import APIRouter

# project
from src.task_tracker.api.v1.tasks import tasks_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(tasks_router)
