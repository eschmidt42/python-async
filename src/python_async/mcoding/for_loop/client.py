import asyncio
import hashlib
import time
import typing as T

import httpx


async def fake_file_data() -> T.AsyncGenerator[bytes, T.Any]:
    yield b"hello, "
    await asyncio.sleep(0.1)  # fake lag
    yield b"world"


async def await_rate_limited(
    awaitables: T.Iterable[T.Awaitable[T.Any]], rate: float
) -> T.AsyncGenerator[T.Any, None]:
    max_sleep_duration = 1 / rate
    for aw in awaitables:
        start = time.perf_counter()
        yield await aw
        elapsed = time.perf_counter() - start
        await asyncio.sleep(max(0.0, max_sleep_duration - elapsed))


async def main():
    async with httpx.AsyncClient() as client:
        # streaming to the starlette server
        response = await client.post(
            "http://127.0.0.1:5000/",
            content=fake_file_data(),
        )
        data = response.read()
        print("Got response:", data.hex())
        print("Expected    :", hashlib.sha256(b"hello, world").hexdigest())

        # rate limited requests to the starlette server
        texts = ["what", "a", "wonderful", "world!"]
        awaitables = (
            client.post("http://127.0.0.1:5000/reverse", json={"text": text})
            for text in texts
        )
        start = time.perf_counter()
        async for result in await_rate_limited(awaitables, rate=2.0):
            elapsed = time.perf_counter() - start
            print(f"[{elapsed:.2f}s] Got result: {result.json()}")


if __name__ == "__main__":
    asyncio.run(main())
