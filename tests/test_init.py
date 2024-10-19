"""Tests for Habiticalib."""

from aiohttp import ClientSession

from habiticalib import Habitica, __version__


async def test_default_user_agent() -> None:
    """Test default user agent is set."""

    async with ClientSession() as session:
        habitica = Habitica(session)
        assert habitica._headers["User-Agent"].startswith(f"Habiticalib/{__version__}")
        assert habitica._headers["User-Agent"].endswith(
            "+https://github.com/tr4nt0r/habiticalib)"
        )
