from fastapi import Request, Response
from fastapi.responses import RedirectResponse as FastAPIRedirectResponse

from .base import BaseExceptionResponse


class ExceptionResponse(BaseExceptionResponse):
    def __init__(self, response: Response):
        self._response = response

    def to_response(self, request: Request) -> Response:
        return self._response


class RedirectResponse(FastAPIRedirectResponse, BaseExceptionResponse):
    def to_response(self, request: Request) -> Response:
        return self
