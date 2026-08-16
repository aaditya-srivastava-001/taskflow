import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class RequestTimingMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        start_time = time.perf_counter()

        response = await call_next(request)

        end_time = time.perf_counter()

        process_time = end_time - start_time

        response.headers["X-Process-Time"] = f"{process_time:.6f}"

        print(
            f"{request.method} "
            f"{request.url.path} "
            f"- {process_time:.6f}s"
        )

        return response