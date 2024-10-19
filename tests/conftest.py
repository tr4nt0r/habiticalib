"""Tests for Habiticalib."""

from collections.abc import Generator
from functools import lru_cache
import pathlib

from aioresponses import aioresponses
import orjson
import pytest


@pytest.fixture(name="mock_aiohttp", autouse=True)
def aioclient_mock() -> Generator[aioresponses]:
    """Mock Aiohttp client requests."""
    with aioresponses() as m:
        yield m


@lru_cache
def load_fixture(filename: str) -> str:
    """Load a fixture."""

    return orjson.loads(
        pathlib.Path(__file__)
        .parent.joinpath("fixtures", filename)
        .read_text(encoding="utf-8")
    )
