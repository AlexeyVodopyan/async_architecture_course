# stdlib
import abc
import logging

# thirdparty
import backoff
import orjson
from aio_pika import Message
from aio_pika import abc as pika_abc
from pydantic import BaseModel

# project
from src.common.messaging.rabbit_base import RabbitClient

logger = logging.getLogger(__name__)


class RabbitProducerFabric(RabbitClient, abc.ABC):
    @staticmethod
    def prepare_body_message(msg: BaseModel) -> bytes:
        """Prepare message body"""
        return orjson.dumps(msg.model_dump())

    @backoff.on_exception(
        backoff.expo, ConnectionError, max_time=10, max_tries=5
    )
    async def produce(self, body: bytes, loop=None, *args, **kwargs):
        """Produce message"""
        async with self.connection(loop=loop) as connection:
            channel = await connection.channel()

            message = await self.get_message(body, *args, **kwargs)

            exchange = await channel.declare_exchange(
                self.exchange, type=pika_abc.ExchangeType.FANOUT, durable=True
            )
            for queue in self.queues:
                queue = await channel.declare_queue(queue, durable=True)
                await queue.bind(exchange)

                await exchange.publish(message, routing_key=queue.name)

                logger.info(
                    "%s: message has been sent to %s"
                    % (self.__class__.__name__, queue)
                )

    @staticmethod
    async def get_message(body: bytes, *args, **kwargs) -> Message:
        """Prediction request message"""
        return Message(
            body=body,
            delivery_mode=pika_abc.DeliveryMode.PERSISTENT,
            *args,
            **kwargs
        )
