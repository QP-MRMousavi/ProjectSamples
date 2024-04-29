from collections.abc import Sequence
from typing import Generic, TypeVar

from pydantic import AnyHttpUrl, BaseModel
from pydantic.generics import GenericModel


class PageParams(BaseModel):
    offset: int
    limit: int
    next: AnyHttpUrl
    previous: AnyHttpUrl


T = TypeVar("T")


class Page(GenericModel, Generic[T]):
    # items: Sequence[T]
    result: Sequence[T]
    # total_pages: int
    count: int
    next: AnyHttpUrl | None = None
    previous: AnyHttpUrl | None = None
