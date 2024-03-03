# stdlib
import abc
import asyncio
from contextlib import asynccontextmanager

# thirdparty
import aio_pika
import backoff
from aio_pika import connect


class RabbitClient(abc.ABC):
    @property
    @abc.abstractmethod
    def queues(self) -> list[str]:
        """queue name"""
        pass

    @property
    @abc.abstractmethod
    def exchange(self) -> str:
        """exchange name"""
        pass

    @property
    @abc.abstractmethod
    def connection_kwargs(self):
        """connection kwargs"""
        pass

    @backoff.on_exception(backoff.constant, ConnectionError, interval=300)
    async def backoff_connect(
        self, connection_kwargs: dict, loop: asyncio.AbstractEventLoop
    ):
        return await connect(
            url=f"amqp://{connection_kwargs['login']}:"
            f"{connection_kwargs['password']}@"
            f"{connection_kwargs['host']}:"
            f"{connection_kwargs['port']}?heartbeat={60 * 60 * 10}",
            loop=loop,
        )

    @asynccontextmanager
    async def connection(
        self, loop: asyncio.AbstractEventLoop
    ) -> aio_pika.RobustConnection:
        connection = await self.backoff_connect(
            self.connection_kwargs,
            loop=loop or asyncio.get_running_loop(),
        )

        async with connection:
            yield connection

            await connection.close()
