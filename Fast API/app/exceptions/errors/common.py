from http import HTTPStatus

from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException

from .base import BaseHttpError


class BadRequest(BaseHttpError):
    @property
    def status_code(self) -> int:
        return HTTPStatus.BAD_REQUEST.value


class Unauthorized(BaseHttpError):
    @property
    def status_code(self) -> int:
        return HTTPStatus.UNAUTHORIZED.value


class Forbidden(BaseHttpError):
    @property
    def status_code(self) -> int:
        return HTTPStatus.FORBIDDEN.value


class NotFound(BaseHttpError):
    @property
    def status_code(self) -> int:
        return HTTPStatus.NOT_FOUND.value


class MethodNotAllowed(BaseHttpError):
    @property
    def status_code(self) -> int:
        return HTTPStatus.METHOD_NOT_ALLOWED.value


class UnprocessableEntity(BaseHttpError):
    @property
    def status_code(self) -> int:
        return HTTPStatus.UNPROCESSABLE_ENTITY.value


class TooManyRequests(BaseHttpError):
    @property
    def status_code(self) -> int:
        return HTTPStatus.TOO_MANY_REQUESTS.value


class InternalServerError(BaseHttpError):
    @property
    def status_code(self) -> int:
        return HTTPStatus.INTERNAL_SERVER_ERROR.value


class InvalidCredentials(Unauthorized):
    pass


class ValidationError(UnprocessableEntity):
    def __init__(self, exc: RequestValidationError):
        super().__init__(
            parameters=[
                {
                    "location": err["loc"],
                    "message": err["msg"],
                    "context": err.get("ctx", {}),
                    "type": err["type"],
                }
                for err in exc.errors()
            ]
        )


class HttpExceptionOverrideError(BaseHttpError):
    def __init__(self, exc: HTTPException):
        self._status_code = exc.status_code
        super().__init__(detail=exc.detail, headers=exc.headers)

    @property
    def status_code(self) -> int:
        return self._status_code
