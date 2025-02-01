"""Tests for user methods of Habiticalib."""

from aiohttp import ClientSession
from aioresponses import aioresponses
import pytest
from syrupy.assertion import SnapshotAssertion
from yarl import URL

from habiticalib import Habitica
from tests.conftest import DEFAULT_HEADERS, TEST_API_KEY, TEST_API_USER


async def test_get_user(snapshot: SnapshotAssertion) -> None:
    """Test get_user method."""

    async with ClientSession() as session:
        habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
        response = await habitica.get_user()
        assert response == snapshot


@pytest.mark.parametrize(
    ("params", "call_params"),
    [
        (["achievements", "items.mounts"], {"userFields": "achievements,items.mounts"}),
        ("achievements,items.mounts", {"userFields": "achievements,items.mounts"}),
    ],
)
async def test_get_user_params(
    mock_aiohttp: aioresponses,
    params: str | list[str] | None,
    call_params: dict[str, str],
) -> None:
    """Test get_user method params."""

    async with ClientSession() as session:
        habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
        await habitica.get_user(params)
        mock_aiohttp.assert_called_with(
            URL("https://habitica.com/api/v3/user"),
            method="get",
            headers=DEFAULT_HEADERS,
            params=call_params,
        )


async def test_get_user_anonymized(snapshot: SnapshotAssertion) -> None:
    """Test get_user_anonymized method."""

    async with ClientSession() as session:
        habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
        response = await habitica.get_user_anonymized()
        assert response == snapshot
