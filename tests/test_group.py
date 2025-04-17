"""Tests group methods of Habiticalib."""

from aiohttp import ClientSession
from syrupy.assertion import SnapshotAssertion

from habiticalib import Habitica
from tests.conftest import TEST_API_KEY, TEST_API_USER


async def test_get_group(snapshot: SnapshotAssertion) -> None:
    """Test get_group method."""

    async with ClientSession() as session:
        habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
        response = await habitica.get_group()
        assert response == snapshot
