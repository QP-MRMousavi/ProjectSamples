from fastapi import Request, Response


class BaseExceptionResponse(Exception):
    def to_response(self, request: Request) -> Response:
        raise NotImplementedError()
