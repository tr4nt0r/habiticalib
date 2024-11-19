"""Tests for user methods of Habiticalib."""

from aiohttp import ClientSession
from aioresponses import aioresponses
from syrupy.assertion import SnapshotAssertion

from habiticalib import Habitica

from .conftest import load_fixture


async def test_login(mock_aiohttp: aioresponses, snapshot: SnapshotAssertion) -> None:
    """Test login."""
    mock_aiohttp.post(
        "https://habitica.com/api/v3/user/auth/local/login",
        body=load_fixture("login.json"),
    )
    async with ClientSession() as session:
        habitica = Habitica(session, "test", "test")
        response = await habitica.login("test-username", "test-password")
        assert response == snapshot


async def test_user(mock_aiohttp: aioresponses, snapshot: SnapshotAssertion) -> None:
    """Test default user agent is set."""
    mock_aiohttp.get("https://habitica.com/api/v3/user", body=load_fixture("user.json"))
    async with ClientSession() as session:
        habitica = Habitica(session, "test", "test")
        response = await habitica.get_user()
        assert response == snapshot
