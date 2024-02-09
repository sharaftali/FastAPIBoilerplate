from contextlib import asynccontextmanager
from typing import AsyncGenerator
import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import Response
from fastapi_injector import InjectorMiddleware, attach_injector
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi.middleware.cors import CORSMiddleware
from injector import Injector
from src.core.di import CoreModule
from src.core.exceptions import (
    handle_internal_exception,
    handle_request_exception,
    handle_validation_exception,
    RequestException,
)
from src.core.middleware import (
    UnitOfWorkMiddleware,
)
from src.core.routers import pre_router
from src.core.schemas import Error
from src.user.di import UserModule

log = logging.getLogger(__name__)

injector = Injector([CoreModule(), UserModule()])
scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    log.debug("==============starting app==================")
    scheduler.start()

    yield
    log.debug("================ending app==================")
    scheduler.shutdown()


async def scheduled_reconcile() -> None:
    log.debug("================calling every minutes==================")
    # use_case = injector.get(ReconcileState)
    # handler = injector.get(ReconcileState.Handler)
    # await reconcile_loop(use_case, handler)


scheduler.add_job(scheduled_reconcile, "interval", minutes=5)

app = FastAPI(
    title="FastAPI Boilerplate API",
    description="FastAPI Boilerplate API",
    version="0.1.0",
    docs_url="/",
    responses={
        404: {
            "model": Error,
            "description": "Not Found",
        },
        422: {
            "model": Error,
            "description": "Validation Error",
        },
    },
    lifespan=lifespan,
)
attach_injector(app, injector)

app.add_middleware(UnitOfWorkMiddleware, injector=injector)
app.add_middleware(InjectorMiddleware, injector=injector)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(pre_router, prefix="/api")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
) -> Response:
    return handle_validation_exception(exc)


@app.exception_handler(RequestException)
async def request_exception_handler(
    request: Request, exc: RequestException
) -> Response:
    return handle_request_exception(exc)


@app.exception_handler(Exception)
async def internal_exception_handler(request: Request, exc: Exception) -> Response:
    return handle_internal_exception(exc)
