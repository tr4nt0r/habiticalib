"""Tests for task method of Habiticalib."""

from datetime import UTC, datetime
from typing import Any
from unittest.mock import AsyncMock
from uuid import UUID

import pytest
from syrupy.assertion import SnapshotAssertion
from yarl import URL

from habiticalib import (
    Attributes,
    Frequency,
    Habitica,
    Repeat,
    Task,
    TaskFilter,
    TaskPriority,
    TaskType,
)
from habiticalib.typedefs import Checklist

from .conftest import DEFAULT_HEADERS, TEST_API_KEY, TEST_API_USER, load_fixture


async def test_get_tasks(snapshot: SnapshotAssertion, session: AsyncMock) -> None:
    """Test get_tasks method."""

    session.request.return_value.__aenter__.return_value.text.return_value = (
        load_fixture("tasks.json")
    )

    habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
    response = await habitica.get_tasks()
    assert response == snapshot


@pytest.mark.parametrize(
    ("params", "call_params"),
    [
        ({"task_type": TaskFilter.DAILYS}, {"type": "dailys"}),
        ({"task_type": TaskFilter.HABITS}, {"type": "habits"}),
        ({"task_type": TaskFilter.REWARDS}, {"type": "rewards"}),
        ({"task_type": TaskFilter.TODOS}, {"type": "todos"}),
        ({"task_type": TaskFilter.COMPLETED_TODOS}, {"type": "completedTodos"}),
        (
            {"due_date": datetime(2024, 10, 15, tzinfo=UTC)},
            {"dueDate": "2024-10-15T00:00:00+00:00"},
        ),
    ],
)
async def test_get_tasks_params(
    session: AsyncMock,
    params: dict[str, Any],
    call_params: dict[str, str],
) -> None:
    """Test get_tasks method parameters."""
    session.request.return_value.__aenter__.return_value.text.return_value = (
        load_fixture("tasks.json")
    )
    habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
    await habitica.get_tasks(**params)
    session.request.assert_called_once_with(
        "GET",
        URL("https://habitica.com/api/v3/tasks/user"),
        headers=DEFAULT_HEADERS,
        params=call_params,
    )


async def test_get_task(snapshot: SnapshotAssertion, session: AsyncMock) -> None:
    """Test get_task method."""
    session.request.return_value.__aenter__.return_value.text.return_value = (
        load_fixture("task.json")
    )

    habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
    response = await habitica.get_task(UUID("7bc0d924-f5e5-48a6-af7f-8075f8c94e0f"))
    assert response == snapshot


@pytest.mark.parametrize(
    ("task", "call_params"),
    [
        (
            Task(
                type=TaskType.DAILY,
                text="text",
                notes="notes",
                completed=False,
                attribute=Attributes.STR,
                alias="alias",
                checklist=[
                    Checklist(
                        id=UUID("fde91e22-fc27-40e6-a861-d2da47b5e7fd"),
                        text="checklist",
                        completed=True,
                    )
                ],
                tags=[
                    UUID("5358c71f-fe0f-4583-84a3-109b70c699fd"),
                    UUID("45870b8b-3e1e-4e13-a722-6afcacdf689f"),
                ],
                collapseChecklist=True,
                priority=TaskPriority.EASY,
                startDate=datetime(2024, 10, 15, tzinfo=UTC),
                frequency=Frequency.WEEKLY,
                everyX=1,
                streak=5,
                repeat=Repeat(),
            ),
            {
                "type": "daily",
                "text": "text",
                "notes": "notes",
                "completed": False,
                "attribute": "str",
                "alias": "alias",
                "checklist": [
                    {
                        "id": "fde91e22-fc27-40e6-a861-d2da47b5e7fd",
                        "text": "checklist",
                        "completed": True,
                    }
                ],
                "tags": [
                    "5358c71f-fe0f-4583-84a3-109b70c699fd",
                    "45870b8b-3e1e-4e13-a722-6afcacdf689f",
                ],
                "collapseChecklist": True,
                "priority": 1,
                "startDate": "2024-10-15T00:00:00+00:00",
                "frequency": "weekly",
                "everyX": 1,
                "streak": 5,
                "repeat": {
                    "m": True,
                    "t": True,
                    "w": True,
                    "th": False,
                    "f": False,
                    "s": False,
                    "su": False,
                },
            },
        ),
        (
            Task(
                type=TaskType.TODO,
                text="text",
                notes="notes",
                checklist=[
                    Checklist(
                        id=UUID("fde91e22-fc27-40e6-a861-d2da47b5e7fd"),
                        text="checklist",
                        completed=True,
                    )
                ],
                priority=TaskPriority.TRIVIAL,
                date=datetime(2024, 10, 15, tzinfo=UTC),
                tags=[
                    UUID("5358c71f-fe0f-4583-84a3-109b70c699fd"),
                    UUID("45870b8b-3e1e-4e13-a722-6afcacdf689f"),
                ],
                alias="alias",
            ),
            {
                "type": "todo",
                "text": "text",
                "notes": "notes",
                "checklist": [
                    {
                        "id": "fde91e22-fc27-40e6-a861-d2da47b5e7fd",
                        "text": "checklist",
                        "completed": True,
                    }
                ],
                "priority": 0.1,
                "date": "2024-10-15T00:00:00+00:00",
                "tags": [
                    "5358c71f-fe0f-4583-84a3-109b70c699fd",
                    "45870b8b-3e1e-4e13-a722-6afcacdf689f",
                ],
                "alias": "alias",
            },
        ),
        (
            Task(
                type=TaskType.HABIT,
                text="text",
                notes="notes",
                priority=TaskPriority.MEDIUM,
                tags=[
                    UUID("5358c71f-fe0f-4583-84a3-109b70c699fd"),
                    UUID("45870b8b-3e1e-4e13-a722-6afcacdf689f"),
                ],
                alias="alias",
                frequency=Frequency.WEEKLY,
                up=True,
                down=True,
                counterUp=1,
                counterDown=1,
            ),
            {
                "type": "habit",
                "text": "text",
                "notes": "notes",
                "priority": 1.5,
                "tags": [
                    "5358c71f-fe0f-4583-84a3-109b70c699fd",
                    "45870b8b-3e1e-4e13-a722-6afcacdf689f",
                ],
                "alias": "alias",
                "frequency": "weekly",
                "up": True,
                "down": True,
                "counterUp": 1,
                "counterDown": 1,
            },
        ),
        (
            Task(
                type=TaskType.REWARD,
                text="text",
                notes="notes",
                value=1.5,
                tags=[
                    UUID("5358c71f-fe0f-4583-84a3-109b70c699fd"),
                    UUID("45870b8b-3e1e-4e13-a722-6afcacdf689f"),
                ],
                alias="alias",
            ),
            {
                "type": "reward",
                "text": "text",
                "notes": "notes",
                "value": 1.5,
                "tags": [
                    "5358c71f-fe0f-4583-84a3-109b70c699fd",
                    "45870b8b-3e1e-4e13-a722-6afcacdf689f",
                ],
                "alias": "alias",
            },
        ),
    ],
    ids=["daily", "todo", "habit", "reward"],
)
async def test_create_task(
    session: AsyncMock,
    task: Task,
    call_params: dict[str, Any],
) -> None:
    """Test create_task method."""
    session.request.return_value.__aenter__.return_value.text.return_value = (
        load_fixture("task.json")
    )
    habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
    await habitica.create_task(task)

    session.request.assert_called_once_with(
        "POST",
        URL("https://habitica.com/api/v3/tasks/user"),
        headers=DEFAULT_HEADERS,
        json=call_params,
    )


async def test_create_task_response(
    snapshot: SnapshotAssertion,
    session: AsyncMock,
) -> None:
    """Test create_task method response."""
    session.request.return_value.__aenter__.return_value.text.return_value = (
        load_fixture("task.json")
    )

    habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
    response = await habitica.create_task(Task(type=TaskType.TODO))
    assert response == snapshot


async def test_update_task(
    session: AsyncMock,
    snapshot: SnapshotAssertion,
) -> None:
    """Test update_task method."""
    session.request.return_value.__aenter__.return_value.text.return_value = (
        load_fixture("task.json")
    )
    habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
    response = await habitica.update_task(
        UUID("7bc0d924-f5e5-48a6-af7f-8075f8c94e0f"), Task(type=TaskType.TODO)
    )
    assert response == snapshot

    session.request.assert_called_once_with(
        "PUT",
        URL("https://habitica.com/api/v3/tasks/7bc0d924-f5e5-48a6-af7f-8075f8c94e0f"),
        headers=DEFAULT_HEADERS,
        json={"type": "todo"},
    )


async def test_delete_task(
    session: AsyncMock,
    snapshot: SnapshotAssertion,
) -> None:
    """Test delete_task method."""
    session.request.return_value.__aenter__.return_value.text.return_value = (
        load_fixture("empty_data.json")
    )

    habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
    response = await habitica.delete_task(UUID("7bc0d924-f5e5-48a6-af7f-8075f8c94e0f"))
    assert response == snapshot

    session.request.assert_called_once_with(
        "DELETE",
        URL("https://habitica.com/api/v3/tasks/7bc0d924-f5e5-48a6-af7f-8075f8c94e0f"),
        headers=DEFAULT_HEADERS,
    )


async def test_reorder_task(
    session: AsyncMock,
    snapshot: SnapshotAssertion,
) -> None:
    """Test reorder_task method."""
    session.request.return_value.__aenter__.return_value.text.return_value = (
        load_fixture("task_order.json")
    )

    habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
    response = await habitica.reorder_task(
        UUID("7bc0d924-f5e5-48a6-af7f-8075f8c94e0f"), 2
    )
    assert response == snapshot

    session.request.assert_called_once_with(
        "POST",
        URL(
            "https://habitica.com/api/v3/tasks/7bc0d924-f5e5-48a6-af7f-8075f8c94e0f/move/to/2"
        ),
        headers=DEFAULT_HEADERS,
    )
