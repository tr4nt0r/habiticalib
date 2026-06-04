"""Tests for login of Habiticalib."""

from unittest.mock import AsyncMock

from syrupy.assertion import SnapshotAssertion

from habiticalib import Habitica

from .conftest import DEFAULT_HEADERS, load_fixture


async def test_login(snapshot: SnapshotAssertion, session: AsyncMock) -> None:
    """Test login and headers."""

    session.request.return_value.__aenter__.return_value.text.return_value = (
        load_fixture("login.json")
    )

    habitica = Habitica(session, "test", "test")
    response = await habitica.login("test-username", "test-password")
    assert response == snapshot
    assert habitica._headers == DEFAULT_HEADERS
