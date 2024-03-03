# thirdparty
from sqlalchemy import Select, Update, select, update

# project
from src.auth.models.user import User
from src.auth.services.users.schemas import UserData


def get_users() -> Select:
    query = select(
        User.email, User.first_name, User.last_name, User.role, User.is_active
    ).order_by(User.modified_at)
    return query


def update_user_data(email: str, data_to_update: UserData) -> Update:
    query = (
        update(User)
        .where(User.email == email)
        .values(
            role=data_to_update.role,
            first_name=data_to_update.first_name,
            last_name=data_to_update.last_name,
            is_active=data_to_update.is_active,
        )
    )
    return query
