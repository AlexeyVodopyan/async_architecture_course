# stdlib
from typing import Optional

# thirdparty
from fastapi import Depends, Security, status
from fastapi.security.api_key import APIKeyHeader
from starlette.requests import Request

# project
from src.auth.services.auth.jwt_auth import JWTAuth, get_jwt_auth
from src.auth.services.auth.schemas import Token
from src.common.schemas.error import ExceptionBody, HTTPException


class ApiKeyHeaderPatched(APIKeyHeader):
    # FastAPI return incorrect status, small patch of this function
    async def __call__(self, request: Request) -> Optional[str]:
        api_key = request.headers.get(self.model.name)
        if not api_key:
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail=ExceptionBody(
                        [
                            {
                                "message": "Not authenticated",
                                "error": "NOT_AUTHENTICATED",
                            }
                        ]
                    ),
                )
            else:
                return None
        return api_key


api_key = ApiKeyHeaderPatched(name="Authorization")


class Authenticated:
    async def __call__(
        self,
        service: JWTAuth = Depends(get_jwt_auth),
        token: str = Security(api_key),
    ) -> tuple[bool, Token]:
        """
        Authorization routine
        """
        email = service.jwt.extract_email_from_token(token)
        validated = False

        if email:
            jwt_secret_key = await service.get_jwt_secret_key(email)

            if jwt_secret_key:
                # token validation
                validated, payload = await service.validate_token(
                    token, jwt_secret_key
                )

        # if token is expired or invalid raise 401
        if not validated:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return validated, payload
