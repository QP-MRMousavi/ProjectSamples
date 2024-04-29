import asyncio
from collections.abc import AsyncGenerator, Generator
from unittest.mock import MagicMock

import pytest
from asgi_lifespan import LifespanManager
from httpx import AsyncClient
from pytest_mock import MockerFixture
from tortoise.backends.base.client import BaseDBAsyncClient

from app import crud, models, schemas
from app.api import deps
from app.core.context import context_db, logger
from app.main import app
from app.tests.utils import new_id, new_random_user, get_specific_user


@pytest.fixture(scope="session")
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with LifespanManager(app=app):
        async with AsyncClient(app=app, base_url="http://test") as client:
            yield client


@pytest.fixture(scope="session")
async def db(async_client: AsyncClient) -> AsyncGenerator[BaseDBAsyncClient, None]:
    async with context_db() as db:
        yield db


@pytest.fixture
def fake_db(
    mocker: MockerFixture,
) -> Generator[MagicMock, None, None]:
    fake_db = MagicMock()
    app.dependency_overrides[deps.get_db] = lambda: fake_db
    yield fake_db
    app.dependency_overrides.pop(deps.get_db)


@pytest.fixture
async def new_rand_user(
    db: BaseDBAsyncClient,
) -> AsyncGenerator[models.User]:

    generated_user, is_created = await crud.user.create_user(
        db=db,
        obj_in=new_user(),
    )
    yield generated_user
    await crud.user.delete_user_by_id(
        db=db,
        obj_data=schemas.UserUpdate(
            id=generated_user.id,
            name=generated_user.name,
            email=generated_user.email,
            password=generated_user.password,
            avatar=generated_user.avatar,
        ),
    )


@pytest.fixture
async def new_specific_user(
    db: BaseDBAsyncClient,
) -> AsyncGenerator[models.User, None]:
    generated_user, is_created = await crud.user.create_user(
        db=db,
        obj_in=get_specific_user(),
    )
    yield generated_user
    await crud.user.delete_user_by_id(
        db=db,
        obj_data=schemas.UserUpdate(
            id=generated_user.id,
            name=generated_user.name,
            email=generated_user.email,
            password=generated_user.password,
            avatar=generated_user.avatar,
        ),
    )
