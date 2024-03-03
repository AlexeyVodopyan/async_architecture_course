# stdlib
from datetime import datetime

# thirdparty
import pydantic
from pydantic import BaseModel, Field


class AuthInput(BaseModel):
    username: str = Field(title="Email")
    password: str = Field(title="Password", min_length=8)


class TokenClaims(BaseModel):
    model_config = pydantic.ConfigDict(
        populate_by_name=True, use_enum_values=True
    )
    email: str | None = Field(title="user email", alias="Email ID")
    role: str


class Token(TokenClaims):
    expiration: datetime = Field(title="Token lifetime", alias="exp")


class TokenPair(BaseModel):
    access: str = Field(title="Access token")
    refresh: str = Field(title="Refresh token")
