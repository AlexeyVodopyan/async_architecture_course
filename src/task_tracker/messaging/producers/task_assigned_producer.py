# project
from src.common.messaging.producers.rabbit_base_producer import (
    RabbitProducerFabric,
)
from src.task_tracker.settings.config import settings


class TaskAssignedProducer(RabbitProducerFabric):
    @property
    def connection_kwargs(self):
        return {
            "host": settings.mq.host,
            "port": settings.mq.port,
            "login": settings.mq.user,
            "password": settings.mq.password,
        }

    @property
    def exchange(self) -> str:
        return settings.mq.task_updates_exchange

    @property
    def queues(self) -> list[str]:
        return [settings.mq.task_assigned_queue]
