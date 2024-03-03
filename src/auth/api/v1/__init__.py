# thirdparty
from fastapi import APIRouter

# project
from src.auth.api.v1.auth import auth_router
from src.auth.api.v1.users import users_router

v1_router = APIRouter(prefix="/v1")
v1_router.include_router(auth_router)
v1_router.include_router(users_router)
