# thirdparty
from sqlalchemy import Insert, Select, insert, select

# project
from src.task_tracker.models import Task, TaskStatus, User


def get_tasks() -> Select:
    query = select(
        Task.name,
        Task.description,
        Task.status,
        Task.assigned_to,
        User.first_name,
        User.last_name,
    ).join(User, User.email == Task.assigned_to)
    return query


def get_users() -> Select:
    query = select(User.first_name, User.last_name, User.email).filter(
        User.is_active.is_(True)
    )
    return query


def insert_task(
    name: str, assigned_to: str, description: str | None
) -> Insert:
    query = insert(Task).values(
        name=name,
        assigned_to=assigned_to,
        description=description,
        status=TaskStatus.OPEN,
    )
    return query
