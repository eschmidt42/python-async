from unittest.mock import MagicMock

import pytest

from python_async.mcoding.generator_pitfall import broken, fixed


@pytest.mark.asyncio
async def test_broken(monkeypatch: pytest.MonkeyPatch):
    "Test that ensures `Resource.__exit__` IS NOT called when the function `broken` terminated."
    mock_resource_instance = MagicMock()

    mock_resource_instance.__enter__.return_value = mock_resource_instance

    mock_resource_class = MagicMock(return_value=mock_resource_instance)

    monkeypatch.setattr(
        "python_async.mcoding.generator_pitfall.Resource", mock_resource_class
    )

    await broken()

    mock_resource_instance.__enter__.assert_called_once()
    mock_resource_instance.__exit__.assert_not_called()


@pytest.mark.asyncio
async def test_fixed(monkeypatch: pytest.MonkeyPatch):
    "Test that ensures `Resource.__exit__` IS called when the function `broken` terminated."
    mock_resource_instance = MagicMock()

    mock_resource_instance.__enter__.return_value = mock_resource_instance

    mock_resource_class = MagicMock(return_value=mock_resource_instance)

    monkeypatch.setattr(
        "python_async.mcoding.generator_pitfall.Resource", mock_resource_class
    )

    await fixed()

    mock_resource_instance.__enter__.assert_called_once()
    mock_resource_instance.__exit__.assert_called_once()
