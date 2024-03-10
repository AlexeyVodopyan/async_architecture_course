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
    host: str | None = Field(
        default="localhost", alias="POSTGRES_HOST_ACCOUNTING"
    )

    port: int | None = Field(default=5431, alias="POSTGRES_PORT_ACCOUNTING")
    db: str | None = Field(
        default="accounting_db", alias="POSTGRES_DB_ACCOUNTING"
    )
    user: str | None = Field(
        default="tasks_admin", alias="POSTGRES_USER_ACCOUNTING"
    )
    password: str | None = Field(
        default="admin", alias="POSTGRES_PASSWORD_ACCOUNTING"
    )


class RabbitMqSettings(BaseSettings):
    host: str | None = Field(default="localhost", alias="RABBITMQ_HOST")
    port: int | None = Field(default=5432, alias="RABBITMQ_PORT")
    user: str | None = Field(default="admin", alias="RABBITMQ_USER")
    password: str | None = Field(default="admin", alias="RABBITMQ_PASSWORD")

    user_updates_exchange: str | None = Field(
        default="user_updates_exchange", alias="RABBITMQ_USER_UPDATES_EXCHANGE"
    )
    user_updates_queue: str | None = Field(
        default="user_updates_tt", alias="RABBITMQ_USER_UPDATES_TT"
    )
    task_updates_exchange: str | None = Field(
        default="task_updates_exchange", alias="RABBITMQ_TASK_UPDATES_EXCHANGE"
    )
    task_created_queue: str | None = Field(
        default="task_created_queue", alias="RABBITMQ_TASK_CREATED_QUEUE"
    )
    task_assigned_queue: str | None = Field(
        default="task_assigned_queue", alias="RABBITMQ_TASK_ASSIGNED_QUEUE"
    )
    task_closed_queue: str | None = Field(
        default="task_closed_queue", alias="RABBITMQ_TASK_CLOSED_QUEUE"
    )


class Settings(BaseSettings):
    db: PostgresSettings
    mq: RabbitMqSettings

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
    return Settings(_env_file=env_file_path, db=db, mq=mq)


settings: Settings = get_settings()
