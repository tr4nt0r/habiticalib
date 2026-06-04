"""Tests for Habiticalib."""

from collections.abc import Generator
from functools import lru_cache
import pathlib
from unittest.mock import AsyncMock, MagicMock, patch

from aiohttp import ClientResponse, ClientSession
import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.image import PNGImageSnapshotExtension
from yarl import URL

from habiticalib.const import DEFAULT_URL

TEST_API_USER = "a380546a-94be-4b8e-8a0b-23e0d5c03303"
TEST_API_KEY = "cd0e5985-17de-4b4f-849e-5d506c5e4382"
DEFAULT_HEADERS = {
    "User-Agent": "Habiticalib/HABITICALIB_VER (OS RELEASE (VERSION); ARCH) aiohttp/AIOHTTP_VER Python/PYTHON_VER  +https://github.com/tr4nt0r/habiticalib)",
    "X-API-KEY": "cd0e5985-17de-4b4f-849e-5d506c5e4382",
    "X-API-USER": "a380546a-94be-4b8e-8a0b-23e0d5c03303",
    "X-CLIENT": "4c4ca53f-c059-4ffa-966e-9d29dd405daf - Habiticalib/HABITICALIB_VER",
}


def pytest_addoption(parser: pytest.Parser) -> None:
    """Commandline options."""

    parser.addoption(
        "--runslow", action="store_true", default=False, help="run slow tests"
    )


def pytest_collection_modifyitems(
    config: pytest.Config,
    items: list[pytest.Item],
) -> None:
    """Check for slow items."""
    if config.getoption("--runslow"):
        # --runslow given in cli: do not skip slow tests
        return

    skip_slow = pytest.mark.skip(reason="need --runslow option to run")
    for item in items:
        if "slow" in item.keywords:
            item.add_marker(skip_slow)


@pytest.fixture
def api_url() -> URL:
    """Return base API URL."""

    return URL(DEFAULT_URL)


@pytest.fixture(autouse=True)
def mock_platform() -> Generator[MagicMock]:
    """Mock platform."""

    with (
        patch("habiticalib.helpers.__version__", "HABITICALIB_VER"),
        patch("habiticalib.helpers.aiohttp.__version__", "AIOHTTP_VER"),
        patch("habiticalib.helpers.platform", autospec=True) as client,
    ):
        client.system.return_value = "OS"
        client.release.return_value = "RELEASE"
        client.version.return_value = "VERSION"
        client.architecture.return_value = ("ARCH", "")
        client.python_version.return_value = "PYTHON_VER"
        yield client


@lru_cache
def load_fixture(filename: str) -> str:
    """Load a fixture."""

    return (
        pathlib.Path(__file__)
        .parent.joinpath("fixtures", filename)
        .read_text(encoding="utf-8")
    )


@lru_cache
def load_bytes_fixture(filename: str) -> bytes:
    """Load a fixture."""

    return pathlib.Path(__file__).parent.joinpath("fixtures", filename).read_bytes()


@pytest.fixture
def snapshot_png(snapshot: SnapshotAssertion) -> SnapshotAssertion:
    """Snapshot PNG."""
    return snapshot.use_extension(PNGImageSnapshotExtension)


@pytest.fixture(name="session")
def mock_session() -> Generator[AsyncMock]:
    """Mock aiohttp ClientSession."""
    mock_session = AsyncMock(spec=ClientSession)
    mock_response = AsyncMock(spec=ClientResponse, status=200)

    mock_session.request.return_value.__aenter__.return_value = mock_response

    return mock_session
