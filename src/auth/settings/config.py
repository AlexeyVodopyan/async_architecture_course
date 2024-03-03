# stdlib
from functools import cache

# thirdparty
from dotenv import find_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings as PydanticSettings
from pydantic_settings import SettingsConfigDict


class BaseSettings(PydanticSettings):
    model_config = SettingsConfigDict(extra="ignore")


class PostgresSettings(BaseSettings):
    host: str | None = Field(default="localhost", alias="POSTGRES_HOST")
    port: int | None = Field(default=5432, alias="POSTGRES_PORT")
    db: str | None = Field(default="auth_db", alias="POSTGRES_DB")
    user: str | None = Field(default="admin", alias="POSTGRES_USER")
    password: str | None = Field(default="admin", alias="POSTGRES_PASSWORD")


class RabbitMqSettings(BaseSettings):
    host: str | None = Field(default="localhost", alias="RABBITMQ_HOST")
    port: int | None = Field(default=5432, alias="RABBITMQ_PORT")
    user: str | None = Field(default="admin", alias="RABBITMQ_USER")
    password: str | None = Field(default="admin", alias="RABBITMQ_PASSWORD")

    exchange: str | None = Field(
        default="users_exchange", alias="RABBITMQ_EXCHANGE"
    )
    task_tracker_queue: str | None = Field(
        default="users_task_tracker_queue", alias="USERS_TASK_TRACKER_QUEUE"
    )


class RedisSettings(BaseSettings):
    host: str | None = Field(default="localhost", alias="REDIS_HOST")
    port: int | None = Field(default=6379, alias="REDIS_PORT")


class Settings(BaseSettings):
    db: PostgresSettings
    mq: RabbitMqSettings
    redis: RedisSettings

    jwt_access_lifetime: int = Field(
        title="access token lifetime, sec",
        default=900,
        alias="JWT_ACCESS_LIFETIME",
    )
    jwt_refresh_lifetime: int = Field(
        title="refresh token lifetime, sec",
        default=14400,
        alias="JWT_REFRESH_LIFETIME",
    )
    jwt_algorithm: str = Field(
        title="JWT encoding algorithm", default="HS256", alias="JWT_ALGORITHM"
    )


def settings_file_path_for_env(env_file_name: str):
    return find_dotenv(env_file_name)


@cache
def get_settings() -> Settings:
    """get current project settings"""

    env_file_path = settings_file_path_for_env(".env")
    db = PostgresSettings(_env_file=env_file_path)
    mq = RabbitMqSettings(_env_file=env_file_path)
    redis = RedisSettings(_env_file=env_file_path)
    return Settings(_env_file=env_file_path, db=db, mq=mq, redis=redis)


settings: Settings = get_settings()
