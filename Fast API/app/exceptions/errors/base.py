import http
import re
from typing import Any

from fastapi import Request
from fastapi.responses import ORJSONResponse

from app.exceptions.base import BaseExceptionResponse
from app.middlewares.access_context import CORRELATION_ID_CTX_KEY

UPPER_CASE_SELECTOR = re.compile(r"(?<!^)(?=[A-Z])")


class BaseHttpError(BaseExceptionResponse):
    def __init__(
        self,
        detail: str | None = None,
        headers: dict[str, str] | None = None,
        **kwargs: Any,
    ):
        self.detail = detail or self.default_detail
        self.headers = headers or {}
        self.extensions = kwargs

    @property
    def type_uri(self) -> str:
        return "about:blank"

    @property
    def status_code(self) -> int:
        raise NotImplementedError()

    @property
    def title(self) -> str:
        return http.HTTPStatus(self.status_code).phrase

    @property
    def default_detail(self) -> str:
        return UPPER_CASE_SELECTOR.sub(" ", self.__class__.__name__).capitalize()

    def to_response(self, request: Request) -> ORJSONResponse:
        """Response with respect to RFC7870."""
        return ORJSONResponse(
            content={
                "type": self.type_uri,
                "status": self.status_code,
                "title": self.title,
                "detail": self.detail,
                "trace_id": request.scope.get(CORRELATION_ID_CTX_KEY, None),
                "extensions": self.extensions,
            },
            status_code=self.status_code,
            headers=self.headers,
            media_type="application/problem+json",
        )


class TypedHttpError(BaseHttpError):
    @property
    def type_uri(self) -> str:
        return self.__class__.__name__
