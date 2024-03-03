# thirdparty
from sqlalchemy import Insert, Select, and_, insert, select

# project
from src.auth.models.user import Role, User


def get_role_pass(email: str) -> Select:
    query = select(User.password, User.role).filter(
        and_(User.email == email, User.is_active.is_(True))
    )
    return query


def insert_user(email: str, password: str, role: Role) -> Insert:
    return insert(User).values(email=email, password=password, role=role)
