from redis import asyncio as aioredis
from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.routing import Route

from starlette_session import SessionMiddleware
from starlette_session.backends import BackendType


async def setup_session(request: Request) -> JSONResponse:
    request.session.update({"data": "session_data"})
    return JSONResponse({"session": request.session})


async def clear_session(request: Request):
    request.session.clear()
    return JSONResponse({"session": request.session})


def view_session(request: Request) -> JSONResponse:
    return JSONResponse({"session": request.session})


routes = [
    Route("/setup_session", endpoint=setup_session),
    Route("/clear_session", endpoint=clear_session),
    Route("/view_session", endpoint=view_session),
]

redis_client = aioredis.from_url("redis://localhost")
app = Starlette(debug=True, routes=routes)
app.add_middleware(
    SessionMiddleware,
    secret_key="secret",
    cookie_name="cookie22",
    backend_type=BackendType.aioRedis,
    backend_client=redis_client,
)
