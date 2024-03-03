# project
from src.auth.settings.config import settings
from src.common.messaging.producers.rabbit_base_producer import (
    RabbitProducerFabric,
)


class UsersUpdatesProducer(RabbitProducerFabric):
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
        return settings.mq.exchange

    @property
    def queues(self) -> list[str]:
        return [settings.mq.task_tracker_queue]
