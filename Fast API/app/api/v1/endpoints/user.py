import datetime
from typing import Any

from fastapi import APIRouter, Depends, Request, Response
from tortoise.backends.base.client import BaseDBAsyncClient

from app import crud, schemas
from app.api import deps
from app.core.configs import settings
from app.core.log import logger

router = APIRouter()


@router.get("/greet", response_model=schemas.Message)
async def greeting(request: Request) -> Any:
    """Greeting something."""
    logger.info(request.headers)
    logger.warning("Greetings", user_id=10)
    return {"message": "hello"}
