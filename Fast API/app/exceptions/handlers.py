from fastapi import FastAPI, Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException

from .base import BaseExceptionResponse
from .errors.common import (
    HttpExceptionOverrideError,
    InternalServerError,
    ValidationError,
)


async def exception_response_handler(
    request: Request, exc: BaseExceptionResponse
) -> Response:
    return exc.to_response(request)


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return HttpExceptionOverrideError(exc).to_response(request)


async def request_validation_error_handler(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    return ValidationError(exc).to_response(request)


async def server_error_handler(request: Request, exc: Exception) -> JSONResponse:
    return InternalServerError().to_response(request)


def add_exception_response_handlers(app: FastAPI) -> None:
    app.add_exception_handler(BaseExceptionResponse, exception_response_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_error_handler)
    app.add_exception_handler(Exception, server_error_handler)
