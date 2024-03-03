# stdlib
import logging

# thirdparty
from fastapi import APIRouter, Depends, status
from jwt import InvalidSignatureError
from sqlalchemy.ext.asyncio import AsyncSession

# project
from src.auth.services.auth.api_service import AuthAPI, get_auth_api_service
from src.auth.services.auth.schemas import AuthInput, TokenClaims, TokenPair
from src.auth.settings.db import get_session

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])
logger = logging.getLogger(__name__)


@auth_router.post(
    path="/sign-up",
    description="User sign up",
    responses={
        status.HTTP_201_CREATED: {"description": "User created"},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid request. "
            "Cause of status will be provided inside the body"
        },
    },
)
async def sign_up(
    auth_input: AuthInput,
    auth_service: AuthAPI = Depends(get_auth_api_service),
    session: AsyncSession = Depends(get_session),
):
    """
    Endpoint for sign up

    Request body:
    **username** - Username
    **password** - Password
    """
    await auth_service.sign_up(
        session=session,
        email=auth_input.username,
        password=auth_input.password,
    )

    return {"message": "User successfully created"}


@auth_router.put(
    path="/sign-in",
    description="Sign user in",
    response_model=TokenPair,
    responses={
        status.HTTP_200_OK: {"description": "User authenticated"},
        status.HTTP_401_UNAUTHORIZED: {"description": "Wrong credentials"},
    },
)
async def sign_in(
    auth_input: AuthInput,
    auth_service: AuthAPI = Depends(get_auth_api_service),
    session: AsyncSession = Depends(get_session),
):
    """
    Endpoint for sign in

    Request body:
    **username** - Username
    **password** - Password
    """
    user_data = await auth_service.login(
        session=session,
        email=auth_input.username,
        password=auth_input.password,
    )

    results: TokenClaims
    access, refresh = await auth_service.generate_token_pair(
        email=user_data.email, role=user_data.role
    )

    return TokenPair(access=access, refresh=refresh)


@auth_router.put(
    path="/sign-out",
    description="Sign user out",
    responses={
        status.HTTP_204_NO_CONTENT: {
            "description": "User has been already signed out"
        },
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid request. Cause of status "
            "will be provided inside the body"
        },
        status.HTTP_200_OK: {"description": "Successfully logged out"},
    },
)
async def sign_out(
    token_pair: TokenPair,
    auth_service: AuthAPI = Depends(get_auth_api_service),
):
    """
    Endpoint for sign out.

    Header has to be generated according to the following format:
    **Authorization: Bearer {access_token} Refresh {refresh token}**
    """
    email = auth_service.jwt_auth.jwt.extract_email_from_token(
        token_pair.access
    )

    if email:
        jwt_secret_key = await auth_service.jwt_auth.get_jwt_secret_key(email)

        if not jwt_secret_key:
            jwt_secret_key = auth_service.jwt_auth.jwt.generate_secret_key()

        try:
            (
                access_decoded,
                refresh_decoded,
            ) = await auth_service.jwt_auth.decode_tokens(
                access_token=token_pair.access,
                refresh_token=token_pair.refresh,
                access_verify=False,
                refresh_verify=False,
                jwt_secret_key=jwt_secret_key,
            )
            await auth_service.jwt_auth.logged_out_tokens(
                (access_decoded, token_pair.access),
                (refresh_decoded, token_pair.refresh),
            )

        except InvalidSignatureError:
            logger.info("Invalid signature error for logout")

    return {"message": "Successfully logged out"}


@auth_router.put(
    path="/refresh",
    description="Refresh tokens",
    response_model=TokenPair,
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "Invalid token(s)"},
        status.HTTP_400_BAD_REQUEST: {
            "description": "Invalid request. Cause of status "
            "will be provided inside the body"
        },
        status.HTTP_200_OK: {"description": "Tokens had been refreshed"},
    },
)
async def refresh_tokens(
    token_pair: TokenPair,
    auth_service: AuthAPI = Depends(get_auth_api_service),
):
    """
    Endpoint for tokens refreshing.

    Header has to be generated according to the following format:
    **Authorization: Bearer {access_token} Refresh {refresh token}**
    """
    access, refresh = await auth_service.jwt_auth.refresh_token(
        access_token=token_pair.access, refresh_token=token_pair.refresh
    )

    return TokenPair(access=access, refresh=refresh)
