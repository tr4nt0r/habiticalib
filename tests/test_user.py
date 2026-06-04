"""Tests for user methods of Habiticalib."""

from unittest.mock import AsyncMock

import pytest
from syrupy.assertion import SnapshotAssertion
from yarl import URL

from habiticalib import Habitica

from .conftest import DEFAULT_HEADERS, TEST_API_KEY, TEST_API_USER, load_fixture


async def test_get_user(snapshot: SnapshotAssertion, session: AsyncMock) -> None:
    """Test get_user method."""
    session.request.return_value.__aenter__.return_value.text.return_value = (
        load_fixture("user.json")
    )

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
    session: AsyncMock,
    params: str | list[str] | None,
    call_params: dict[str, str],
) -> None:
    """Test get_user method params."""

    session.request.return_value.__aenter__.return_value.text.return_value = (
        load_fixture("user.json")
    )

    habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
    await habitica.get_user(params)
    session.request.assert_called_once_with(
        "GET",
        URL("https://habitica.com/api/v3/user"),
        headers=DEFAULT_HEADERS,
        params=call_params,
    )


async def test_get_user_anonymized(
    snapshot: SnapshotAssertion, session: AsyncMock
) -> None:
    """Test get_user_anonymized method."""

    session.request.return_value.__aenter__.return_value.text.return_value = (
        load_fixture("user_anonymized.json")
    )

    habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
    response = await habitica.get_user_anonymized()
    assert response == snapshot
