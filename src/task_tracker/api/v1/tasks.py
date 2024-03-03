# stdlib
import logging

# thirdparty
from fastapi import APIRouter, Depends, status

tasks_router = APIRouter(prefix="/tasks", tags=["Tasks"])
logger = logging.getLogger(__name__)
