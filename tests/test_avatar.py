"""Tests for avatar generator of Habiticalib."""

import asyncio
from io import BytesIO
import pathlib
import sys

from aiohttp import ClientSession
from aioresponses import aioresponses
import pytest
from syrupy.assertion import SnapshotAssertion
from yarl import URL

from habiticalib import Avatar, Habitica

from .conftest import load_fixture


@pytest.mark.skipif(sys.platform != "linux", reason="needs linux")
@pytest.mark.slow
async def test_generate_avatar(
    mock_aiohttp: aioresponses,
    snapshot: SnapshotAssertion,
    snapshot_png: SnapshotAssertion,
    api_url: URL,
) -> None:
    """Test generation of avatar from user response."""
    # workaround due to qs double-encoding by aioresponses
    url = str(api_url / "api/v3/user") + "?userFields=preferences%2Citems%2Cstats"
    mock_aiohttp.get(url, body=load_fixture("user.json"))

    async with ClientSession() as session:
        habitica = Habitica(session, "test", "test")
        avatar = BytesIO()

        response = await habitica.generate_avatar(avatar, fmt="png")
        assert response == snapshot
        assert avatar.getvalue() == snapshot_png


@pytest.mark.skipif(sys.platform != "linux", reason="needs linux")
@pytest.mark.slow
async def test_generate_avatar_to_file(
    mock_aiohttp: aioresponses,
    api_url: URL,
    tmp_path: pathlib.Path,
    snapshot_png: SnapshotAssertion,
) -> None:
    """Test saving avatar to file."""
    # workaround due to qs double-encoding by aioresponses
    url = str(api_url / "api/v3/user") + "?userFields=preferences%2Citems%2Cstats"
    mock_aiohttp.get(url, body=load_fixture("user.json"))

    async with ClientSession() as session:
        habitica = Habitica(session, "test", "test")

        avatar = tmp_path / "avatar.png"

        await habitica.generate_avatar(str(avatar), fmt="png")
        await asyncio.sleep(0.1)  # wait a bit till saving avatar task settles
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(None, avatar.read_bytes)
        assert result == snapshot_png


@pytest.mark.parametrize(
    ("style_variations"),
    [
        "user_styles.json",
        "user_styles_with_chair.json",
        "user_styles_kickstarter.json",
        "user_styles_kickstarter_pets.json",
        "user_styles_sleeping.json",
        "user_styles_spookySparkles.json",
        "user_styles_shinySeed.json",
        "user_styles_snowball.json",
        "user_styles_seafoam.json",
        "user_styles_special_0.json",
        "user_styles_special_1.json",
        "user_styles_weapon_critical.json",
        "user_styles_animated_background.json",
    ],
    ids=[
        "default",
        "with_chair",
        "kickstarter_backer_gear",
        "kickstarter_pet_mount",
        "sleeping",
        "spookySparkles",
        "shinySeed",
        "snowball",
        "seafoam",
        "special_0",
        "special_1",
        "weapon_critical",
        "animated_background",
    ],
)
@pytest.mark.usefixtures("mock_aiohttp")
@pytest.mark.skipif(sys.platform != "linux", reason="needs linux")
@pytest.mark.slow
async def test_generate_avatar_from_styles(
    snapshot_png: SnapshotAssertion,
    style_variations: str,
) -> None:
    """Test generation of avatar from avatar object."""

    avatar = Avatar.from_json(load_fixture(style_variations))
    async with ClientSession() as session:
        habitica = Habitica(session, "test", "test")
        avatar_png = BytesIO()

        response = await habitica.generate_avatar(avatar_png, avatar, fmt="png")

        assert response == avatar
        assert avatar_png.getvalue() == snapshot_png
