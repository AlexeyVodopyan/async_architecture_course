# thirdparty
from pydantic import ConfigDict, RootModel

# project
from src.common.schemas.user_updates_schemas import UserData


class Users(RootModel):
    model_config = ConfigDict(orm_mode=True)
    root: list[UserData]
