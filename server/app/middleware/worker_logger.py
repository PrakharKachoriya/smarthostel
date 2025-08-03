import os
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

class WorkerLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        pid = os.getpid()
        print(f"[Worker PID: {pid}] Handling request: {request.method} {request.url}")
        response: Response = await call_next(request)
        return response