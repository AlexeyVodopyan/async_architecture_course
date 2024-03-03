# stdlib
import functools
import secrets
from datetime import datetime, timedelta, timezone

# thirdparty
import jwt
from fastapi import HTTPException, status
from pydantic import ValidationError

# project
from src.auth.services.auth.schemas import Token
from src.auth.settings.config import settings


class JWTGenerator:
    @staticmethod
    def extract_email_from_token(access_token: str) -> str | None:
        """Extracts email from token"""
        try:
            decoded_token = jwt.decode(
                access_token, options={"verify_signature": False}
            )
        except jwt.exceptions.DecodeError:
            return None
        return decoded_token.get("Email ID")

    @staticmethod
    def generate_secret_key() -> str:
        return secrets.token_hex(32)

    @staticmethod
    def generate_token(lifetime: int, jwt_secret_key: str, **kwargs) -> str:
        """Generates token"""
        try:
            claims = Token(
                expiration=(
                    datetime.now(tz=timezone.utc) + timedelta(seconds=lifetime)
                ).timestamp(),
                **kwargs
            )
        except ValidationError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        token = jwt.encode(
            payload=claims.model_dump(by_alias=True),
            algorithm=settings.jwt_algorithm,
            key=jwt_secret_key,
        )

        return token

    @staticmethod
    def decode(token: str, jwt_secret_key: str, **kwargs) -> Token | None:
        """Decodes token"""
        decoded = jwt.decode(
            jwt=token,
            key=jwt_secret_key,
            algorithms=settings.jwt_algorithm,
            **kwargs
        )

        try:
            return Token.model_validate(decoded)
        except ValidationError:
            return None


@functools.cache
def get_jwt_generator():
    return JWTGenerator()
