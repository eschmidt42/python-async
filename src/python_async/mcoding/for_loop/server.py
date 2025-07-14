import hashlib
import logging
import typing as T

from starlette.applications import Starlette
from starlette.requests import Request
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Route

logger = logging.getLogger(__name__)


async def online_sha256(stream: T.AsyncGenerator[bytes, None]) -> bytes:
    hasher = hashlib.sha256()
    async for chunk in stream:
        logger.info(f"got chunk: {chunk}")
        hasher.update(chunk)
    return hasher.digest()


async def compute_sha256(request: Request) -> PlainTextResponse:
    bytes_hash = await online_sha256(request.stream())
    return PlainTextResponse(bytes_hash)


async def get_reverse(request: Request) -> JSONResponse:
    try:
        body = await request.json()
        logger.info(f"{body=}")
        # Example: reverse a string field called 'text'
        if isinstance(body, dict) and "text" in body:
            reversed_text = body["text"][::-1]
            return JSONResponse({"reversed": reversed_text})
        else:
            return JSONResponse({"error": "Missing 'text' field"}, status_code=400)
    except Exception as e:
        logger.info(f"Error decoding JSON: {e}")
        return JSONResponse({"error": "Invalid JSON"}, status_code=400)


routes = [
    Route(path="/", endpoint=compute_sha256, methods=["POST"]),
    Route(path="/reverse", endpoint=get_reverse, methods=["POST"]),
]

app = Starlette(debug=True, routes=routes)


def main():
    import uvicorn
    from uvicorn.config import LOGGING_CONFIG

    log_config = dict(LOGGING_CONFIG)

    log_config["loggers"]["python_async"] = {
        "handlers": ["default"],
        "level": "INFO",
        "propagate": True,
    }
    log_config["loggers"][""] = {
        "handlers": ["default"],
        "level": "INFO",
        "propagate": True,
    }

    uvicorn.run(app, port=5000, log_config=log_config)  # log_level="info"


if __name__ == "__main__":
    main()
