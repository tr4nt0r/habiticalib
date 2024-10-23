# Habiticalib

<p align="center">
    <em>Modern asynchronous Python client library for the Habitica API</em>
</p>

[![build](https://github.com/tr4nt0r/habiticalib/workflows/Build/badge.svg)](https://github.com/tr4nt0r/habiticalib/actions)
[![codecov](https://codecov.io/gh/tr4nt0r/habiticalib/graph/badge.svg?token=iEsZ1Ktj7d)](https://codecov.io/gh/tr4nt0r/habiticalib)
[![PyPI version](https://badge.fury.io/py/habiticalib.svg)](https://badge.fury.io/py/habiticalib)

**Habiticalib** is a Python library for interacting with the [Habitica API](https://habitica.com). It provides an organized, typed interface to work with Habitica’s features, including tasks, user data, and avatars. The goal of this library is to simplify integration with Habitica.

## Key features

- **Asynchronous**: The library is fully asynchronous, allowing non-blocking API calls.
- **Fully typed with Dataclasses**: The library is fully typed using Python `dataclasses`. It handles serialization with `mashumaro` and `orjson` for efficient conversion between Habitica API JSON data and Python objects.
- **Dynamic avatar image generation**: Habiticalib can fetch all necessary assets (like equipped items, pets, and mounts) and combine them into a single avatar image. This image can be saved to disk or returned as a byte buffer for further processing.
 **Fetch user data**: Retrieve and manage user data such as stats, preferences, and items. User data is structured with dataclasses to make it easy to work with.
- **Task management**: Support for creating, updating, and retrieving Habitica tasks (to-dos, dailies, habits, rewards) is provided.
- **Task status updates**: The library allows updates for task statuses, habit scoring, and daily completion.
- **Tags**: Habiticalib supports the creation, updating and deletion of tags.
-  **Stat allocation, class cystem and sleep**: The library offers methods for stat point allocation and switching between Habitica classes. It also provides the ability to disable the class system and pausing damage(resting in the inn)

## Installation

```bash
pip install habiticalib
```

## Getting started
Here’s an example to demonstrate basic usage:

```python
import asyncio

from aiohttp import ClientSession

from habiticalib import Habitica, TaskType


async def main():
    async with ClientSession() as session:
       habitica = Habitica(session)

       # Login to Habitica
       habitica.login(username="your_username", password="your_password")

       # Fetch user data
       user_data = await habitica.user()
       print(f"Your current health: {user_data.stats.hp}")

        # Fetch all tasks (to-dos, dailies, habits, and rewards)
        tasks = await habitica.get_tasks()
        print("All tasks:")
        for task in tasks:
            print(f"- {task.text} (type: {task.type})")

        # Fetch only to-dos
        todos = await habitica.get_tasks(task_type=TaskType.TODO)
        print("\nTo-Do tasks:")
        for todo in todos:
            print(f"- {todo.text} (due: {todo.date})")

        # Fetch only dailies
        dailies = await habitica.tasks(task_type=TaskType.DAILY)
        print("\nDailies:")
        for daily in dailies:
            print(f"- {daily.text}")

asyncio.run(main())
```

## Documentation

For full documentation and detailed usage examples, please visit the [Habiticalib documentation](https://tr4nt0r.github.io/habiticalib/).

## License

This project is licensed under the terms of the MIT license.
