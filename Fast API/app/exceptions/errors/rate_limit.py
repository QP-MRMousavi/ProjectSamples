from http import HTTPStatus
from typing import Any

from .base import TypedHttpError


# TODO: Add redis for rate limiting
class RateLimited(TypedHttpError):
    def __init__(
        self,
        detail: str | None = None,
        retry_after: int | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ):
        super().__init__(detail=detail, headers=headers, **kwargs)
        if retry_after is not None:
            self.headers["Retry-After"] = str(retry_after)

    @property
    def status_code(self) -> int:
        return HTTPStatus.TOO_MANY_REQUESTS.value
