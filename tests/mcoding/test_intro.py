import pytest
from pyleak import no_task_leaks
from pyleak.base import LeakAction

from python_async.mcoding import intro


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "func",
    [
        intro.do_loop_v1,
        intro.do_loop_v2,
        intro.do_loop_v3,
        intro.do_loop_v4,
    ],
)
async def test_do_loops_run_without_errors(func, caplog):
    todo = ["task1", "task2", "task3"]
    with caplog.at_level("INFO"):
        await func(todo)

    # Check that logs contain "started" and "done" for each task
    for item in todo:
        assert any(f"work: {item} started" in m for m in caplog.messages)
        assert any(f"work: {item} done" in m for m in caplog.messages)


@pytest.mark.asyncio
async def test_do_work_logs(caplog):
    with caplog.at_level("INFO"):
        await intro.do_work("test", delay_s=0.01)
    assert any("work: test started" in m for m in caplog.messages)
    assert any("work: test done" in m for m in caplog.messages)


@pytest.mark.asyncio
async def test_main_tasks():
    async with no_task_leaks(action=LeakAction.RAISE):
        await intro.main()
