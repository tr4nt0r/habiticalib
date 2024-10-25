"""Tests for Habiticalib."""

from collections.abc import Generator
from functools import lru_cache
import pathlib

from aioresponses import CallbackResult, aioresponses
import pytest
from yarl import URL

from habiticalib.const import ASSETS_URL, DEFAULT_URL


@pytest.fixture
def api_url() -> URL:
    """Return base API URL."""

    return URL(DEFAULT_URL)


def load_assets_fixture(url: URL, **kwargs) -> CallbackResult:
    """Load assets callback."""
    asset = pathlib.Path(url.path).name
    return CallbackResult(body=load_bytes_fixture(asset))


@pytest.fixture(name="mock_aiohttp", autouse=True)
def aioclient_mock() -> Generator[aioresponses]:
    """Mock Aiohttp client requests."""
    with aioresponses(passthrough=[ASSETS_URL]) as m:
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
