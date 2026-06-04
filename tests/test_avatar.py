"""Tests for avatar generator of Habiticalib."""

import asyncio
from io import BytesIO
import pathlib
import sys
from unittest.mock import patch

from aiohttp import ClientSession
import pytest
from syrupy.assertion import SnapshotAssertion

from habiticalib import Avatar, Habitica, HabiticaUserResponse

from .conftest import load_fixture


@pytest.mark.skipif(sys.platform != "linux", reason="needs linux")
@pytest.mark.slow
async def test_generate_avatar(
    snapshot: SnapshotAssertion,
    snapshot_png: SnapshotAssertion,
) -> None:
    """Test generation of avatar from user response."""

    avatar = BytesIO()

    with patch(
        "habiticalib.Habitica.get_user",
        return_value=HabiticaUserResponse.from_json(load_fixture("user.json")),
    ):
        async with ClientSession() as session:
            habitica = Habitica(session, "test", "test")
            response = await habitica.generate_avatar(avatar, fmt="png")

    assert response == snapshot
    assert avatar.getvalue() == snapshot_png


@pytest.mark.skipif(sys.platform != "linux", reason="needs linux")
@pytest.mark.slow
async def test_generate_avatar_to_file(
    tmp_path: pathlib.Path,
    snapshot_png: SnapshotAssertion,
) -> None:
    """Test saving avatar to file."""
    avatar = tmp_path / "avatar.png"

    with patch(
        "habiticalib.Habitica.get_user",
        return_value=HabiticaUserResponse.from_json(load_fixture("user.json")),
    ):
        async with ClientSession() as session:
            habitica = Habitica(session, "test", "test")
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
