import datetime

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.routing import APIRoute
from tortoise.backends.base.client import BaseDBAsyncClient

from app import crud, middlewares
from app.api.v1 import api_router
from app.core import security
from app.core.configs import settings
from app.core.context import (
    start_db,
    stop_db,
)
from app.exceptions import add_exception_response_handlers


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{list(route.methods)[0].lower()}_{route.name}"


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json",
    generate_unique_id_function=custom_generate_unique_id,
    swagger_ui_parameters={"syntaxHighlight": True},
    docs_url=f"{settings.API_V1_PREFIX}/docs",
    version=settings.API_VERSION,
)

app.add_middleware(middlewares.MetricsMiddleware)
app.add_middleware(middlewares.AccessContextLogMiddleware)
# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
app.add_middleware(GZipMiddleware, minimum_size=1000, compresslevel=9)
add_exception_response_handlers(app)


@app.on_event("startup")
async def startup() -> None:
    app.state.db = await start_db()


@app.on_event("shutdown")
async def shutdown() -> None:
    await stop_db(app.state.db)


app.include_router(api_router, prefix=settings.API_V1_PREFIX)
