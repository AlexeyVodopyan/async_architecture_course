# stdlib
import logging

# thirdparty
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.auth.services.auth.auth_checker import Authenticated
from src.auth.services.users.api_service import UsersAPI, get_users_api_service
from src.auth.services.users.schemas import Users
from src.auth.settings.db import get_session
from src.common.schemas.v1.user_updates_schemas import UserUpdateEventData

users_router = APIRouter(
    prefix="/users",
    tags=["Authentication"],
    dependencies=[Depends(Authenticated())],
)

logger = logging.getLogger(__name__)


@users_router.get(
    path="",
    description="Get list of users",
    response_model=Users,
    responses={
        status.HTTP_200_OK: {"description": "List of users"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Not Authorized"},
    },
)
async def users_list(
    users_service: UsersAPI = Depends(get_users_api_service),
    session: AsyncSession = Depends(get_session),
):
    """
    Get list of users
    """
    result = await users_service.get_users_list(session=session)
    return result


@users_router.put(
    path="/{email}",
    description="Update user info",
    responses={
        status.HTTP_200_OK: {"description": "Successfully updated"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Not Authorized"},
    },
)
async def update_user(
    email: str,
    updated_data: UserUpdateEventData,
    users_service: UsersAPI = Depends(get_users_api_service),
    session: AsyncSession = Depends(get_session),
):
    """
    Get list of users
    """
    await users_service.update_user_info(session, email, updated_data)
    return {"detail": "Successfully updated"}
