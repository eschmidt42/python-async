# https://youtu.be/ftmdDlwMwwQ?si=iwQDccvArQb55bbk
# https://github.com/mCodingLLC/VideosSampleCode/blob/master/videos/117_hello_async/boring_async.py

import asyncio
import logging
import time

logger = logging.getLogger(__name__)


async def do_work(s: str, delay_s: float = 1.0):
    logger.info(f"work: {s} started")
    await asyncio.sleep(delay_s)
    logger.info(f"work: {s} done")


async def do_loop_v1(todo):
    tasks = [asyncio.create_task(do_work(item)) for item in todo]
    done, _ = await asyncio.wait(tasks)
    for task in done:
        _ = task.result()


async def do_loop_v2(todo):
    tasks = [asyncio.create_task(do_work(item)) for item in todo]
    _ = await asyncio.gather(*tasks, return_exceptions=True)


async def do_loop_v3(todo):
    coros = [do_work(item) for item in todo]
    _ = await asyncio.gather(*coros, return_exceptions=True)


async def do_loop_v4(todo):
    async with asyncio.TaskGroup() as tg:
        _ = [tg.create_task(do_work(item)) for item in todo]


async def main():
    start = time.perf_counter()

    todo = ["get package", "laundry", "bake cake"]

    await do_loop_v1(todo)

    await do_loop_v2(todo)

    await do_loop_v3(todo)

    await do_loop_v4(todo)

    end = time.perf_counter()
    logger.info(f"it took: {end - start:.2f}s")


if __name__ == "__main__":
    logging.basicConfig(
        format="%(asctime)s %(module)s.py %(funcName)s %(levelname)s: %(message)s",
        level=logging.INFO,
    )

    asyncio.run(main())
