# stdlib
import abc
import asyncio
import logging
import traceback
import typing

# thirdparty
import pydantic
from aio_pika.abc import ExchangeType

# project
from src.common.messaging.rabbit_base import RabbitClient

logger = logging.getLogger(__name__)


class RabbitConsumerFabric(RabbitClient, abc.ABC):
    def __init__(self, prefetch_count: int):
        self.prefetch_count = prefetch_count
        self.channel = None

    @property
    def queue(self) -> str:
        """Queue to consume"""
        return self.queues[0]

    @property
    @abc.abstractmethod
    def msg_model(self) -> typing.Type[pydantic.BaseModel]:
        """Message data model type"""

    @abc.abstractmethod
    async def main_action(self, msg, *args, **kwargs):
        """Actions related to received message"""

    @staticmethod
    async def validation_error_handling():
        """Validation error handling"""
        logger.error(traceback.format_exc())

    def parse_message(self, message: bytes) -> pydantic.BaseModel:
        """Method for message parsing"""
        return self.msg_model.parse_raw(message)

    async def consume(self, loop: asyncio.AbstractEventLoop, *args, **kwargs):
        async with self.connection(loop=loop) as connection:
            self.channel = await connection.channel()

            await self.channel.set_qos(prefetch_count=self.prefetch_count)

            exchange = await self.channel.declare_exchange(
                self.exchange, type=ExchangeType.FANOUT, durable=True
            )
            queue = await self.channel.declare_queue(self.queue, durable=True)
            await queue.bind(exchange, routing_key=self.queue)

            logger.info(
                "%s: start consuming messages from %s"
                % (self.__class__.__name__, self.queue)
            )

            async with queue.iterator() as queue_iter:
                async for msg in queue_iter:
                    async with msg.process():
                        # parsing part
                        logger.info(
                            "%s: message received" % self.__class__.__name__
                        )
                        try:
                            parsed_msg = self.parse_message(message=msg.body)
                        except pydantic.ValidationError:
                            await self.validation_error_handling()
                            continue

                        # postprocessing part
                        try:
                            await self.main_action(msg=parsed_msg)
                        except Exception as e:
                            await self.handle_error(error=e, msg=parsed_msg)

    @staticmethod
    async def handle_error(error, msg, *args, **kwargs):
        logger.exception("Could not consume message %s" % error)
