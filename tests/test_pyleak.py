import asyncio

import pytest
from pyleak import TaskLeakError, no_task_leaks
from pyleak.base import LeakAction


async def leaking_func():
    # Start a background task that never completes
    asyncio.create_task(asyncio.sleep(10))


@pytest.mark.asyncio
async def test_no_task_leaks_raises_on_leaked_task():
    with pytest.raises(TaskLeakError):
        # no_task_leaks should raise because leaking_func leaks a task
        async with no_task_leaks(action=LeakAction.RAISE):
            await leaking_func()
