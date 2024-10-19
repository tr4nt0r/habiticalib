"""Tests for Habiticalib."""

from collections.abc import Generator

from aioresponses import aioresponses
import pytest


@pytest.fixture(name="mock_aiohttp", autouse=True)
def aioclient_mock() -> Generator[aioresponses]:
    """Mock Aiohttp client requests."""
    with aioresponses() as m:
        yield m
