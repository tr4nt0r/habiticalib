"""Tests serialization of typedefs."""

import pytest
from syrupy.assertion import SnapshotAssertion

from habiticalib import (
    HabiticaLoginResponse,
    HabiticaResponse,
    HabiticaTaskResponse,
    HabiticaTasksResponse,
    HabiticaUserAnonymizedResponse,
    HabiticaUserResponse,
)
from habiticalib.typedefs import HabiticaTaskOrderResponse

from .conftest import load_fixture


@pytest.mark.parametrize(
    ("fixture", "resp_class"),
    [
        ("login.json", HabiticaLoginResponse),
        ("task.json", HabiticaTaskResponse),
        ("tasks.json", HabiticaTasksResponse),
        ("user_anonymized.json", HabiticaUserAnonymizedResponse),
        ("user.json", HabiticaUserResponse),
        ("task_order.json", HabiticaTaskOrderResponse),
        ("empty_data.json", HabiticaResponse),
    ],
)
async def test_serialize(
    snapshot: SnapshotAssertion,
    fixture: str,
    resp_class: type[HabiticaResponse],
) -> None:
    """Test serialization of Habitica response classes."""

    assert resp_class.from_json(load_fixture(fixture)).to_dict() == snapshot
