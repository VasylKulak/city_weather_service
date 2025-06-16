import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request

from app.router import router
from app.setup.dynamo_db import create_table_if_not_exists
from app.setup.logger import configure_logging


@asynccontextmanager
async def lifespan(app: FastAPI):
    configure_logging()
    create_table_if_not_exists()

    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router)


logger = logging.getLogger(__name__)


@app.middleware("http")
async def log_exceptions_middleware(request: Request, call_next):
    """
    Middleware for logging.
    """
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"URL: {request.url} - Exception: {e}", exc_info=True)
        raise e
