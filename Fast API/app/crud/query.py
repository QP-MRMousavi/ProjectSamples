from typing import Any, TypeVar

from tortoise.backends.base.client import BaseDBAsyncClient
from tortoise.queryset import QuerySet

from app.models.base import Base
from app.schemas.pagination import PageParams

BaseT = TypeVar("BaseT", bound="Base")


async def paginate(
    db: BaseDBAsyncClient, page_params: PageParams, query: QuerySet[BaseT]
) -> dict[str, Any]:
    count = await query.using_db(db).count()
    result = await query.using_db(db).offset(page_params.offset).limit(page_params.limit)
    return {
        "result": result,
        "count": count,
        "next": page_params.next
        if page_params.offset + page_params.limit < count
        else None,
        "previous": page_params.previous
        if page_params.offset - page_params.limit >= 0
        else None,
    }
