from __future__ import annotations

from timeit import default_timer

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint

from app.core.log import logger


class MetricsMiddleware(BaseHTTPMiddleware):

    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """
        This method is a middleware that measures the performance of HTTP requests.

        Parameters:
        - request (Request): The incoming HTTP request.
        - call_next (RequestResponseEndpoint): A coroutine that represents the next middleware or the main application.

        Returns:
        - Response: The HTTP response after processing the request.

        Raises:
        - Exception: If an error occurs during the request processing.

        This method records the following metrics:
        - method: The HTTP method used in the request (e.g., GET, POST).
        - status_code: The HTTP status code of the response.
        - handler: The path of the handler that processed the request.
        - duration: The time taken to process the request, in seconds.
        - request_size: The size of the request, in bytes.
        - response_size: The size of the response, in bytes.

        The metrics are recorded in the `http_metrics` object.
        """
        start_time = default_timer()
        status_code = 500
        response_size = 0
        try:
            response = await call_next(request)
            status_code = response.status_code
            response_size = int(response.headers.get("Content-Length", 0))
            return response
        finally:
            app_metrics = {
                "method": request.method,
                "status_code": status_code,
                "handler": (
                    request.scope["route"].path
                    if "route" in request.scope
                    else request.url.path
                ),
                "duration": max(default_timer() - start_time, 0),
                "request_size": int(request.headers.get("Content-Length", 0)),
                "response_size": response_size,
            }

            logger.info(app_metrics)
