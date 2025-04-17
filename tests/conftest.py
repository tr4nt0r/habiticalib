"""Tests for Habiticalib."""

from collections.abc import Generator
from functools import lru_cache
import pathlib
import re
from unittest.mock import MagicMock, patch

from aioresponses import CallbackResult, aioresponses
import pytest
from syrupy.assertion import SnapshotAssertion
from syrupy.extensions.image import PNGImageSnapshotExtension
from yarl import URL

from habiticalib.const import ASSETS_URL, DEFAULT_URL

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


def load_assets_fixture(url: URL, **kwargs) -> CallbackResult:
    """Load assets callback."""
    asset = pathlib.Path(url.path).name
    return CallbackResult(body=load_bytes_fixture(asset))


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


@pytest.fixture(name="mock_aiohttp", autouse=True)
def aioclient_mock() -> Generator[aioresponses]:
    """Mock Aiohttp client requests."""
    with aioresponses(passthrough=[ASSETS_URL]) as m:
        m.post(
            "https://habitica.com/api/v3/user/auth/local/login",
            body=load_fixture("login.json"),
        )
        m.get(
            re.compile(r"^https://habitica\.com/api/v3/user.*$"),
            body=load_fixture("user.json"),
        )
        m.get(
            "https://habitica.com/api/v3/user/anonymized",
            body=load_fixture("user_anonymized.json"),
        )
        m.get(
            re.compile(r"^https://habitica\.com/api/v3/tasks/user\?.*$"),
            body=load_fixture("tasks.json"),
        )
        m.get(
            "https://habitica.com/api/v3/tasks/user",
            body=load_fixture("tasks.json"),
        )
        m.post(
            "https://habitica.com/api/v3/tasks/user",
            body=load_fixture("task.json"),
        )
        m.get(
            "https://habitica.com/api/v3/tasks/7bc0d924-f5e5-48a6-af7f-8075f8c94e0f",
            body=load_fixture("task.json"),
        )
        m.put(
            "https://habitica.com/api/v3/tasks/7bc0d924-f5e5-48a6-af7f-8075f8c94e0f",
            body=load_fixture("task.json"),
        )
        m.delete(
            "https://habitica.com/api/v3/tasks/7bc0d924-f5e5-48a6-af7f-8075f8c94e0f",
            body=load_fixture("empty_data.json"),
        )
        m.post(
            "https://habitica.com/api/v3/tasks/7bc0d924-f5e5-48a6-af7f-8075f8c94e0f/move/to/2",
            body=load_fixture("task_order.json"),
        )
        m.get(
            "https://habitica.com/api/v3/groups/party",
            body=load_fixture("party.json"),
        )

        yield m


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
