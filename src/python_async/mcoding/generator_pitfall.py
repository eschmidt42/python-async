"""
>>> python src/python_async/mcoding/generator_pitfall.py
broken:
yield 0
got 0
yield 1
got 1
cleanup: outer resource
after loop

fixed:
yield 0
got 0
yield 1
got 1
got exc:  GeneratorExit
cleanup: inner resource
cleanup: outer resource
after loop
got exc:  CancelledError
cleanup: inner resource

So with plain `async for x in gen():` the inner resource is never cleaned up / or after the outer resource -> unexpected.

To prevent this one can use `async with contextlib.aclosing(gen()) as g:` which raises a BaseException when the outer loop is terminated.
"""

import asyncio
import contextlib
import typing as T


class Resource:
    def __init__(self, name: str):
        self.name = name

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print(f"cleanup: {self.name}")


async def gen() -> T.AsyncGenerator[int, T.Any]:
    with Resource("inner resource"):
        for x in range(3):
            print(f"yield {x}")
            try:
                yield x
            except BaseException as exc:
                print("got exc: ", type(exc).__name__)
                raise


async def fixed():
    async with contextlib.aclosing(gen()) as g:
        async for x in g:
            print(f"got {x}")
            if x == 1:
                break


async def broken():
    async for x in gen():
        print(f"got {x}")
        if x == 1:
            break


async def main():
    print("broken:")
    with Resource("outer resource"):
        await broken()
    print("after loop")

    print("\nfixed:")
    with Resource("outer resource"):
        await fixed()
    print("after loop")


if __name__ == "__main__":
    asyncio.run(main())
