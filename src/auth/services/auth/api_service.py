# stdlib
import functools
import logging

# thirdparty
from fastapi import status
from pydantic import EmailStr
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.auth.messaging.producers.user_updates_producer import (
    UsersUpdatesProducer,
)
from src.auth.models.user import Role
from src.auth.services.auth.jwt_auth import JWTAuth, get_jwt_auth
from src.auth.services.auth.queries import get_role_pass, insert_user
from src.auth.services.auth.schemas import TokenClaims
from src.common.schemas.error import ExceptionBody, HTTPException
from src.common.schemas.user_updates_schemas import (
    ActionType,
    UserData,
    UserUpdateMessage,
)

logger = logging.getLogger(__name__)


class AuthAPI:
    def __init__(self):
        self.jwt_auth: JWTAuth = get_jwt_auth()
        self.user_updates_producer = UsersUpdatesProducer()

    @staticmethod
    async def _check_user(
        session: AsyncSession,
        email: EmailStr | str,
        password: str,
    ) -> TokenClaims:
        query = get_role_pass(email)
        result = await session.execute(query)
        user_info = result.one()

        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=ExceptionBody(
                    [
                        {
                            "message": "Invalid credentials",
                            "error": "WRONG_CREDENTIALS",
                        }
                    ]
                ),
            )

        is_auth = user_info[0] == password

        if is_auth:
            return TokenClaims(
                email=email,
                role=user_info[1],
            )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ExceptionBody(
                [
                    {
                        "message": "Invalid credentials",
                        "error": "WRONG_CREDENTIALS",
                    }
                ]
            ),
        )

    async def login(
        self,
        session: AsyncSession,
        email: str,
        password: str,
    ) -> TokenClaims:
        """
        Check user credentials
        """
        user_info = await self._check_user(
            session=session,
            email=email,
            password=password,
        )
        return user_info

    async def _send_update_to_mq(
        self, action: ActionType, email: str, role: Role
    ):
        msg = UserUpdateMessage(
            action=action,
            data=UserData(email=email, role=role, is_active=True),
        )
        msg_bytes = self.user_updates_producer.prepare_body_message(msg)
        await self.user_updates_producer.produce(msg_bytes)

    async def sign_up(
        self,
        session: AsyncSession,
        email: str,
        password: str,
    ):
        """
        Create new user
        """
        query = insert_user(email, password, Role.PARROT)

        try:
            await session.execute(query)
            await session.commit()
        except IntegrityError as e:
            logger.error(e)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ExceptionBody(
                    [
                        {
                            "message": "User already exists",
                            "error": "USER_ALREADY_EXISTS",
                        }
                    ]
                ),
            )
        await self._send_update_to_mq(ActionType.created, email, Role.PARROT)

    async def drop_token(self, username: str):
        """Drop secret"""
        await self.jwt_auth.delete_secret([username])

    async def generate_token_pair(self, email, **kwargs):
        return await self.jwt_auth.generate_token_pair(email, **kwargs)


@functools.cache
def get_auth_api_service():
    return AuthAPI()
