import pytest
from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.exceptions import DoesNotExist

from collections.abc import AsyncGenerator, Generator
from httpx import AsyncClient
from app.core.context import context_db, logger

from app.models.user import User
from app.schemas.user import (
    UserCreate,
    UserUpdate,
)
from app.crud import user as crud_user
from app.tests.utils import new_id, new_random_user, get_specific_user


# Test case for creating a new user successfully
@pytest.mark.asyncio
async def test_create_user_success(db: BaseDBAsyncClient):
    user_data = get_specific_user()
    created_user, created = await crud_user.create_user(db=db, obj_data=user_data)
    assert created_user is not None
    assert created


# Test case for attempting to create a user with an existing email
@pytest.mark.asyncio
async def test_create_user_existing_email(db: BaseDBAsyncClient):

    existing_user_data = get_specific_user()
    await crud_user.create_user(db=db, obj_data=existing_user_data)

    # Attempt to create a user with the same email
    new_user_data = get_specific_user()
    created_user, created = await crud_user.create_user(db=db, obj_data=new_user_data)
    assert created_user is None
    assert not created
