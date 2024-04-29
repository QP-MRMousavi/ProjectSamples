import datetime
from collections.abc import Awaitable, Sequence
from typing import Any, Generic, TypeVar, get_args

import orjson
from pydantic import BaseModel, ValidationError
from tortoise.backends.base.client import BaseDBAsyncClient

from app.core.log import logger
from app.models.base import Base

ModelT = TypeVar("ModelT", bound=Base)
CreateSchemaT = TypeVar("CreateSchemaT", bound=BaseModel)
UpdateSchemaT = TypeVar("UpdateSchemaT", bound=BaseModel)


class CRUDBase(Generic[ModelT, CreateSchemaT, UpdateSchemaT]):
    def __init__(self) -> None:
        generic_bases = getattr(self, "__orig_bases__", ())
        if not generic_bases:
            raise RuntimeError("Object class is not a valid generic")
        self.model: type[ModelT] = get_args(generic_bases[0])[0]

    async def all(self, db: BaseDBAsyncClient) -> list[ModelT]:
        return await self.model.all().using_db(db)

    async def get(self, db: BaseDBAsyncClient, *, record_id: Any) -> ModelT | None:
        return await self.model.filter(id=record_id).using_db(db).first()

    async def get_multi(
        self,
        db: BaseDBAsyncClient,
        *,
        ids: Sequence[Any],
        prefetch_related: list[str] | None = None,
    ) -> dict[Any, ModelT]:
        return {
            rec.id: rec
            for rec in await self.model.filter(id__in=ids)
            .using_db(db)
            .prefetch_related(*(prefetch_related or []))
        }

    async def create(
        self,
        db: BaseDBAsyncClient,
        *,
        obj_in: CreateSchemaT,
    ) -> ModelT:
        record = self.model(**obj_in.dict())
        await record.save(using_db=db)
        return record

    async def _update(
        self,
        db: BaseDBAsyncClient,
        *,
        db_obj: ModelT,
        obj_in: dict[str, Any],
    ) -> ModelT:
        db_obj._set_kwargs(obj_in)
        await db_obj.save(using_db=db, update_fields=obj_in.keys())
        return db_obj

    async def update(
        self,
        db: BaseDBAsyncClient,
        *,
        db_obj: ModelT,
        obj_in: UpdateSchemaT,
    ) -> ModelT:
        return await self._update(
            db,
            db_obj=db_obj,
            obj_in=obj_in.dict(exclude_unset=True),
        )

    async def update_changes_only(
        self,
        db: BaseDBAsyncClient,
        *,
        db_obj: ModelT,
        obj_in: UpdateSchemaT,
    ) -> ModelT:
        obj_in_dict = obj_in.dict(exclude_unset=True)
        changes = {
            key: obj_in_dict[key]
            for key, val in db_obj.__dict__.items()
            if key in obj_in_dict and obj_in_dict[key] != val
        }
        if not changes:
            return db_obj
        return await self._update(
            db,
            db_obj=db_obj,
            obj_in=changes,
        )

    async def delete(self, db: BaseDBAsyncClient, *, db_obj: ModelT) -> None:
        return await db_obj.delete(using_db=db)

    async def delete_by_id(self, db: BaseDBAsyncClient, *, record_id: Any) -> int:
        return await self.model.filter(id=record_id).using_db(db).delete()

    async def fetch_all_related(
        self,
        db: BaseDBAsyncClient,
        *,
        db_obj: ModelT,
    ) -> ModelT:
        await db_obj.fetch_related(*db_obj._meta.fetch_fields)
        return db_obj
