# stdlib
import logging.config
import os
from contextlib import asynccontextmanager

# thirdparty
import uvicorn
from fastapi import FastAPI

# project
from src.auth.api import api_router
from src.common.logging_config import LOGGING_CONFIG

logger = logging.getLogger(__name__)
logging.config.dictConfig(LOGGING_CONFIG)


@asynccontextmanager
async def lifespan(_: FastAPI):
    logger.info(
        "AUTH SERVICE "
        "SUCCESSFULLY STARTED WITH VERSION"
        " {}".format(os.getenv("AUTH_CONTAINER_VERSION"))
    )

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
        port=8000,
        log_config=LOGGING_CONFIG,
    )
