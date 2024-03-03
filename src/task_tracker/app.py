# stdlib
import asyncio
import logging.config
import os
from contextlib import asynccontextmanager

# thirdparty
import uvicorn
from fastapi import FastAPI

# project
from src.common.logging_config import LOGGING_CONFIG
from src.task_tracker.api import api_router
from src.task_tracker.messaging.consumers.user_updates_consumer import (
    UsersUpdatesConsumer,
)

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING_CONFIG)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info(
        "TASK TRACKER SERVICE "
        "SUCCESSFULLY STARTED WITH VERSION"
        " {}".format(os.getenv("TASK_CONTAINER_VERSION"))
    )

    loop = asyncio.get_event_loop()

    # new consumers
    user_updates_consumer = UsersUpdatesConsumer()
    loop.create_task(user_updates_consumer.consume(loop))

    yield


def create_app(lifespan_, main_router):
    application = FastAPI(lifespan=lifespan_)
    application.include_router(main_router)
    return application


if __name__ == "__main__":
    app = create_app(lifespan, api_router)

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8001,
        log_config=LOGGING_CONFIG,
        use_colors=False,
    )
