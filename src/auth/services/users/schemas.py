# thirdparty
from pydantic import ConfigDict, RootModel

# project
from src.common.schemas.v1.user_updates_schemas import UserUpdateEventData


class Users(RootModel):
    model_config = ConfigDict(from_attributes=True)
    root: list[UserUpdateEventData]
