import pytest
from inline_snapshot import snapshot
from pyleak import no_task_leaks
from pyleak.base import LeakAction
from starlette.testclient import TestClient

from python_async.mcoding.for_loop.client import fake_file_data
from python_async.mcoding.for_loop.server import app, online_sha256

client = TestClient(app)


def test_compute_sha256_basic():
    data = b"hello world"
    response = client.post("/", content=data)
    assert response.status_code == 200
    assert response.content == snapshot(
        b"\xb9M'\xb9\x93M>\x08\xa5.R\xd7\xda}\xab\xfa\xc4\x84\xef\xe3zS\x80\xee\x90\x88\xf7\xac\xe2\xef\xcd\xe9"
    )


def test_get_reverse_valid_text():
    response = client.post("/reverse", json={"text": "hello"})
    assert response.status_code == 200
    assert response.json() == snapshot({"reversed": "olleh"})


@pytest.mark.asyncio
async def test_online_sha256_single_chunk():
    async with no_task_leaks(action=LeakAction.RAISE):
        result = await online_sha256(fake_file_data())

    assert result == snapshot(
        b"\t\xca~N\xaan\x8a\xe9\xc7\xd2a\x16q)\x18H\x83dM\x07\xdf\xba|\xbf\xbcL\x8a.\x086\r["
    )
