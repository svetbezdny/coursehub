from collections.abc import AsyncGenerator, Awaitable, Callable
from contextlib import asynccontextmanager
from uuid import uuid4

from fastapi import FastAPI, Request, Response
from starlette.types import Lifespan

from app.config import settings
from app.database import async_session_maker, seed_database
from app.exception_handlers import register_exception_handlers
from app.routers import routers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    await seed_database(async_session_maker)
    yield


def create_app(*, lifespan_handler: Lifespan[FastAPI] = lifespan) -> FastAPI:
    app = FastAPI(
        title=settings.app_title,
        description=settings.app_description,
        version=settings.app_version,
        lifespan=lifespan_handler,
    )

    @app.middleware("http")
    async def add_request_id(
        request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        request_id = request.headers.get(settings.request_id_header) or uuid4().hex
        response = await call_next(request)
        response.headers[settings.request_id_header] = request_id
        return response

    register_exception_handlers(app)

    for router in routers:
        app.include_router(router)

    return app


app = create_app()
