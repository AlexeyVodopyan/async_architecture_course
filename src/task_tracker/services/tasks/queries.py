# stdlib
import uuid

# thirdparty
from sqlalchemy import Insert, Select, Update, insert, select, update

# project
from src.task_tracker.models import Task, TaskStatus, User


def get_tasks() -> Select:
    query = select(
        Task.id,
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
    name: str, assigned_to: str, description: str | None, public_id: uuid.UUID
) -> Insert:
    query = insert(Task).values(
        public_id=public_id,
        name=name,
        assigned_to=assigned_to,
        description=description,
        status=TaskStatus.OPEN,
    )
    return query


def close_task(
    task_id: uuid.UUID,
) -> Update:
    query = (
        update(Task)
        .where(Task.id == task_id, Task.status == TaskStatus.OPEN)
        .values(
            status=TaskStatus.CLOSED,
        )
        .returning(Task.name, Task.assigned_to, Task.public_id)
    )
    return query
