"""Tests for login of Habiticalib."""

from aiohttp import ClientSession
from syrupy.assertion import SnapshotAssertion

from habiticalib import Habitica

from .conftest import DEFAULT_HEADERS


async def test_login(snapshot: SnapshotAssertion) -> None:
    """Test login and headers."""

    async with ClientSession() as session:
        habitica = Habitica(session, "test", "test")
        response = await habitica.login("test-username", "test-password")
        assert response == snapshot
        assert habitica._headers == DEFAULT_HEADERS
