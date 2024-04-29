from http import HTTPStatus

from .base import TypedHttpError


class Duplicated(TypedHttpError):
    @property
    def status_code(self) -> int:
        return HTTPStatus.BAD_REQUEST.value
