# Habiticalib

Modern asynchronous Python client library for the Habitica API

[![build](https://github.com/tr4nt0r/habiticalib/workflows/Build/badge.svg)](https://github.com/tr4nt0r/habiticalib/actions)
[![codecov](https://codecov.io/gh/tr4nt0r/habiticalib/graph/badge.svg?token=iEsZ1Ktj7d)](https://codecov.io/gh/tr4nt0r/habiticalib)
[![PyPI version](https://badge.fury.io/py/habiticalib.svg)](https://badge.fury.io/py/habiticalib)
![PyPI - Downloads](https://img.shields.io/pypi/dm/habiticalib?style=flat&label=pypi%20downloads)
[!["Buy Me A Coffee"](https://img.shields.io/badge/-buy_me_a%C2%A0coffee-gray?logo=buy-me-a-coffee)](https://www.buymeacoffee.com/tr4nt0r)
[![GitHub Sponsor](https://img.shields.io/badge/GitHub-Sponsor-blue?logo=github)](https://github.com/sponsors/tr4nt0r)

---

**Habiticalib** is a Python library for interacting with the [Habitica API](https://habitica.com). It provides an organized, typed interface to work with Habitica’s features, including tasks, user data, and avatars. The goal of this library is to simplify integration with Habitica.

## Key features

* **Asynchronous**: The library is fully asynchronous, allowing non-blocking API calls.
* **Fully typed with Dataclasses**: The library is fully typed using Python `dataclasses`. It handles serialization with `mashumaro` and `orjson` for efficient conversion between Habitica API JSON data and Python objects.
* **Dynamic avatar image generation**: Habiticalib can fetch all necessary assets (like equipped items, pets, and mounts) and combine them into a single avatar image. This image can be saved to disk or returned as a byte buffer for further processing.
* **Fetch user data**: Retrieve and manage user data such as stats, preferences, and items. User data is structured with dataclasses to make it easy to work with.
* **Task management**: Support for creating, updating, and retrieving Habitica tasks (to-dos, dailies, habits, rewards) is provided.
* **Task status updates**: The library allows updates for task statuses, habit scoring, and daily completion.
* **Tags**: Habiticalib supports the creation, updating and deletion of tags.
* **Stat allocation, class cystem and sleep**: The library offers methods for stat point allocation and switching between Habitica classes. It also provides the ability to disable the class system and pausing damage(resting in the inn)

---

## 📖 Documentation

* **Full Documentation**: [https://tr4nt0r.github.io/habiticalib](https://tr4nt0r.github.io/habiticalib)
* **Source Code**: [https://github.com/tr4nt0r/habiticalib](https://github.com/tr4nt0r/habiticalib)

---

## 📦 Installation

```bash
pip install habiticalib
```

## 🚀 Getting started

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

---

## 🛠️ Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch.
3. Make your changes and commit them.
4. Submit a pull request.

Make sure to follow the [contributing guidelines](CONTRIBUTING.md).

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## ❤️ Support

If you find this project useful, consider [buying me a coffee ☕](https://www.buymeacoffee.com/tr4nt0r) or [sponsoring me on GitHub](https://github.com/sponsors/tr4nt0r)!
