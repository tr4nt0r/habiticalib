"""Tests group methods of Habiticalib."""

from unittest.mock import AsyncMock

from syrupy.assertion import SnapshotAssertion

from habiticalib import Habitica

from .conftest import TEST_API_KEY, TEST_API_USER, load_fixture


async def test_get_group(snapshot: SnapshotAssertion, session: AsyncMock) -> None:
    """Test get_group method."""
    session.request.return_value.__aenter__.return_value.text.return_value = (
        load_fixture("party.json")
    )

    habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
    response = await habitica.get_group()
    assert response == snapshot
