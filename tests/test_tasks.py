"""Tests for task method of Habiticalib."""

from datetime import UTC, datetime
from typing import Any
from uuid import UUID

from aiohttp import ClientSession
from aioresponses import aioresponses
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

from .conftest import DEFAULT_HEADERS, TEST_API_KEY, TEST_API_USER


async def test_get_tasks(snapshot: SnapshotAssertion) -> None:
    """Test get_tasks method."""

    async with ClientSession() as session:
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
    mock_aiohttp: aioresponses,
    params: dict[str, Any],
    call_params: dict[str, str],
) -> None:
    """Test get_tasks method parameters."""

    async with ClientSession() as session:
        habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
        await habitica.get_tasks(**params)
        mock_aiohttp.assert_called_with(
            URL("https://habitica.com/api/v3/tasks/user"),
            method="get",
            headers=DEFAULT_HEADERS,
            params=call_params,
        )


async def test_get_task(snapshot: SnapshotAssertion) -> None:
    """Test get_task method."""

    async with ClientSession() as session:
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
    mock_aiohttp: aioresponses,
    task: Task,
    call_params: dict[str, Any],
) -> None:
    """Test create_task method."""

    async with ClientSession() as session:
        habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
        await habitica.create_task(task)

        mock_aiohttp.assert_called_with(
            URL("https://habitica.com/api/v3/tasks/user"),
            method="post",
            headers=DEFAULT_HEADERS,
            json=call_params,
        )


async def test_create_task_response(
    snapshot: SnapshotAssertion,
) -> None:
    """Test create_task method response."""

    async with ClientSession() as session:
        habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
        response = await habitica.create_task(Task(type=TaskType.TODO))
        assert response == snapshot


async def test_update_task(
    mock_aiohttp: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test update_task method."""

    async with ClientSession() as session:
        habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
        response = await habitica.update_task(
            UUID("7bc0d924-f5e5-48a6-af7f-8075f8c94e0f"), Task(type=TaskType.TODO)
        )
        assert response == snapshot

        mock_aiohttp.assert_called_with(
            URL(
                "https://habitica.com/api/v3/tasks/7bc0d924-f5e5-48a6-af7f-8075f8c94e0f"
            ),
            method="put",
            headers=DEFAULT_HEADERS,
            json={"type": "todo"},
        )


async def test_delete_task(
    mock_aiohttp: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test delete_task method."""

    async with ClientSession() as session:
        habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
        response = await habitica.delete_task(
            UUID("7bc0d924-f5e5-48a6-af7f-8075f8c94e0f")
        )
        assert response == snapshot

        mock_aiohttp.assert_called_with(
            URL(
                "https://habitica.com/api/v3/tasks/7bc0d924-f5e5-48a6-af7f-8075f8c94e0f"
            ),
            method="delete",
            headers=DEFAULT_HEADERS,
        )


async def test_reorder_task(
    mock_aiohttp: aioresponses,
    snapshot: SnapshotAssertion,
) -> None:
    """Test reorder_task method."""

    async with ClientSession() as session:
        habitica = Habitica(session, TEST_API_USER, TEST_API_KEY)
        response = await habitica.reorder_task(
            UUID("7bc0d924-f5e5-48a6-af7f-8075f8c94e0f"), 2
        )
        assert response == snapshot

        mock_aiohttp.assert_called_with(
            URL(
                "https://habitica.com/api/v3/tasks/7bc0d924-f5e5-48a6-af7f-8075f8c94e0f/move/to/2"
            ),
            method="post",
            headers=DEFAULT_HEADERS,
        )
