"""Modern asynchronous Python client library for the Habitica API."""

from __future__ import annotations

import asyncio
from http import HTTPStatus
from io import BytesIO
import logging
from typing import IO, TYPE_CHECKING, Self

from aiohttp import ClientError, ClientResponseError, ClientSession
from PIL import Image
from yarl import URL

from .const import ASSETS_URL, BACKER_ONLY_GEAR, DEFAULT_URL
from .exceptions import (
    BadRequestError,
    NotAuthorizedError,
    NotFoundError,
    TooManyRequestsError,
)
from .helpers import extract_user_styles, get_user_agent, get_x_client, join_fields
from .types import (
    Attributes,
    Class,
    Direction,
    HabiticaClassSystemResponse,
    HabiticaErrorResponse,
    HabiticaLoginResponse,
    HabiticaResponse,
    HabiticaScoreResponse,
    HabiticaStatsResponse,
    HabiticaTagResponse,
    HabiticaTagsResponse,
    HabiticaTaskOrderResponse,
    HabiticaTaskResponse,
    HabiticaTasksResponse,
    HabiticaUserExport,
    HabiticaUserResponse,
    Language,
    Skill,
    Task,
    TaskFilter,
    UserStyles,
)

if TYPE_CHECKING:
    from datetime import datetime
    from uuid import UUID

_LOGGER = logging.getLogger(__package__)


class Habitica:
    """Modern asynchronous Python client library for the Habitica API."""

    _close_session: bool = False
    _cache_size = 32

    def __init__(
        self,
        session: ClientSession | None = None,
        api_user: str | None = None,
        api_key: str | None = None,
        url: str | None = None,
        x_client: str | None = None,
    ) -> None:
        """Initialize the Habitica API client."""
        client_headers = {"X-CLIENT": get_x_client(x_client)}
        user_agent = {"User-Agent": get_user_agent()}
        self._headers: dict[str, str] = {}

        if session:
            self._session = session
            if "User-Agent" not in session.headers:
                self._headers.update(user_agent)
            self._headers.update(client_headers)
        else:
            self._session = ClientSession(
                headers={**user_agent, **client_headers},
            )
            self._close_session = True

        if api_user and api_key:
            self._headers.update(
                {
                    "X-API-USER": api_user,
                    "X-API-KEY": api_key,
                }
            )
        elif api_user or api_key:
            msg = "Both 'api_user' and 'api_key' must be provided together."
            raise ValueError(msg)

        self.url = URL(url if url else DEFAULT_URL)

        self._assets_cache: dict[str, IO[bytes]] = {}
        self._cache_order: list[str] = []

    async def _request(self, method: str, url: URL, **kwargs) -> str:
        """Handle API request."""
        async with self._session.request(
            method,
            url,
            headers=self._headers,
            **kwargs,
        ) as r:
            if r.status == HTTPStatus.UNAUTHORIZED:
                raise NotAuthorizedError(
                    HabiticaErrorResponse.from_json(await r.text()), r.headers
                )
            if r.status == HTTPStatus.NOT_FOUND:
                raise NotFoundError(
                    HabiticaErrorResponse.from_json(await r.text()), r.headers
                )
            if r.status == HTTPStatus.BAD_REQUEST:
                raise BadRequestError(
                    HabiticaErrorResponse.from_json(await r.text()), r.headers
                )
            if r.status == HTTPStatus.TOO_MANY_REQUESTS:
                raise TooManyRequestsError(
                    HabiticaErrorResponse.from_json(await r.text()), r.headers
                )
            r.raise_for_status()
            return await r.text()

    async def __aenter__(self) -> Self:
        """Async enter."""
        return self

    async def __aexit__(self, *exc_info: object) -> None:
        """Async exit."""
        if self._close_session:
            await self._session.close()

    async def login(
        self,
        username: str,
        password: str,
    ) -> HabiticaLoginResponse:
        """Log in a user using their email or username and password.

        This method sends a POST request to the Habitica API to authenticate
        a user. Upon successful authentication, it updates the headers with
        the user's API credentials for future requests.

        Parameters
        ----------
        username : str
            The user's email or username used for logging in.
        password : str
            The user's password for authentication.

        Returns
        -------
        HabiticaLoginResponse
            An object containing the user's authentication details, including
            user ID and API token.

        Raises
        ------
        NotAuthorizedError
            If the login request fails due to incorrect username or password (HTTP 401).
        aiohttp.ClientResponseError
            For other HTTP-related errors raised by aiohttp, such as HTTP 400 or 500.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        >>> response = await habitica.login("username_or_email", "password")
        >>> response.data.id
        'user-id'
        >>> response.data.apiToken
        'api-token'
        """
        url = self.url / "api/v3/user/auth/local/login"
        data = {
            "username": username,
            "password": password,
        }

        response = HabiticaLoginResponse.from_json(
            await self._request("post", url=url, data=data),
        )
        self._headers.update(
            {
                "X-API-USER": str(response.data.id),
                "X-API-KEY": str(response.data.apiToken),
            },
        )
        return response

    async def get_user(
        self,
        user_fields: str | list[str] | None = None,
        *,
        anonymized: bool = False,
    ) -> HabiticaUserResponse:
        """Get the authenticated user's profile.

        Parameters
        ----------
        user_fields : str | list[str] | None, optional
            A string or a list of fields to include in the response.
            If provided as a list, the fields will be joined with commas.
            If None, the full user profile document is returned. Default is None.
        anonymized : bool
            When True, returns the user's data without: Authentication information,
            New Messages/Invitations/Inbox, Profile, Purchased information,
            Contributor information, Special items, Webhooks, Notifications.
            (default is False)

        Returns
        -------
        HabiticaUserResponse
            A response object containing the result of the API call.

        Raises
        ------
        NotAuthorizedError
            If the API request is unauthorized (HTTP 401).
        aiohttp.ClientResponseError
            For other HTTP-related errors raised by aiohttp, such as HTTP 400 or 500.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        >>> response = await habitica.get_user(user_fields="achievements,items.mounts")
        >>> response.data  # Access the returned data from the response
        """
        url = self.url / "api/v3/user"
        params = {}

        if user_fields:
            params = {"userFields": join_fields(user_fields)}
        if anonymized:
            url = url / "anonymized"

        return HabiticaUserResponse.from_json(
            await self._request("get", url=url, params=params),
        )

    async def get_tasks(
        self,
        task_type: TaskFilter | None = None,
        due_date: datetime | None = None,
    ) -> HabiticaResponse:
        """Get the authenticated user's tasks.

        Parameters
        ----------
        task_type : TaskFilter | None
            The type of task to retrieve, defined in TaskFilter enum.
            If `None`, all task types will be retrieved (default is None).

        due_date : datetime | None
            Optional date to use for computing the nextDue field for each returned task.

        Returns
        -------
        HabiticaResponse
            A response object containing the user's tasks, parsed from the JSON
            response.

        Raises
        ------
        NotAuthorizedError
            If the API request is unauthorized (HTTP 401).
        aiohttp.ClientResponseError
            For other HTTP-related errors raised by aiohttp, such as HTTP 400 or 500.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        Retrieve all tasks:

        >>> await habitica.get_tasks()

        Retrieve only todos:

        >>> await habitica.get_tasks(TaskType.HABITS)

        Retrieve todos with a specific due date:

        >>> await habitica.get_tasks(TaskType.HABITS, due_date=datetime(2024, 10, 15))
        """
        url = self.url / "api/v3/tasks/user"
        params = {}

        if task_type:
            params.update({"type": task_type.value})
        if due_date:
            params.update({"dueDate": due_date.isoformat()})
        return HabiticaTasksResponse.from_json(
            await self._request("get", url=url, params=params),
        )

    async def get_task(self, task_id: UUID) -> HabiticaTaskResponse:
        """Retrieve a specific task from the Habitica API.

        This method sends a request to the Habitica API to retrieve a specific task
        identified by the given `task_id`.

        Parameters
        ----------
        task_id : UUID
            The UUID of the task to retrieve.

        Returns
        -------
        HabiticaTaskResponse
            A response object containing the data for the specified task.

        Raises
        ------
        aiohttp.ClientResponseError
            For HTTP-related errors, such as HTTP 400 or 500 response status.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        >>> task_id = UUID("12345678-1234-5678-1234-567812345678")
        >>> task_response = await habitica.get_task(task_id)
        >>> print(task_response.data)  # Displays the retrieved task information
        """
        url = self.url / "api/v3/tasks" / str(task_id)

        return HabiticaTaskResponse.from_json(
            await self._request("get", url=url),
        )

    async def create_task(self, task: Task) -> HabiticaTaskResponse:
        """Create a new task in the Habitica API.

        This method sends a request to the Habitica API to create a new task
        with the specified attributes defined in the `task` object.

        Parameters
        ----------
        task : Task
            An instance of the `Task` dataclass containing the attributes for the new task.

        Returns
        -------
        HabiticaTaskResponse
            A response object containing the data for the newly created task.

        Raises
        ------
        aiohttp.ClientResponseError
            For HTTP-related errors, such as HTTP 400 or 500 response status.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        >>> new_task = Task(name="New Task", ...)
        >>> create_response = await habitica.create_task(new_task)
        >>> print(create_response.data)  # Displays the created task information
        """
        url = self.url / "api/v3/tasks/user"

        return HabiticaTaskResponse.from_json(
            await self._request("post", url=url, json=task.to_dict()),
        )

    async def update_task(self, task_id: UUID, task: Task) -> HabiticaTaskResponse:
        """Update an existing task in the Habitica API.

        This method sends a request to the Habitica API to update the attributes
        of a specific task identified by the given `task_id` with the specified
        attributes defined in the `task` object.

        Parameters
        ----------
        task_id : UUID
            The UUID of the task to update.
        task : Task
            An instance of the `Task` dataclass containing the updated attributes for the task.

        Returns
        -------
        HabiticaTaskResponse
            A response object containing the data of the updated task.

        Raises
        ------
        aiohttp.ClientResponseError
            For HTTP-related errors, such as HTTP 400 or 500 response status.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        >>> task_id = UUID("12345678-1234-5678-1234-567812345678")
        >>> updated_task = Task(name="Updated Task", ...)
        >>> update_response = await habitica.update_task(task_id, updated_task)
        >>> print(update_response.data)  # Displays the updated task information
        """
        url = self.url / "api/v3/tasks" / str(task_id)

        return HabiticaTaskResponse.from_json(
            await self._request("put", url=url, json=task.to_dict()),
        )

    async def delete_task(self, task_id: UUID) -> HabiticaResponse:
        """Delete a specific task.

        This method sends a request to the Habitica API to delete a specific task
        identified by the given `task_id`.

        Parameters
        ----------
        task_id : UUID
            The UUID of the task to delete.

        Returns
        -------
        HabiticaTaskResponse
            A response object containing the data for the deleted task.

        Raises
        ------
        aiohttp.ClientResponseError
            For HTTP-related errors, such as HTTP 400 or 500 response status.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        >>> task_id = UUID("12345678-1234-5678-1234-567812345678")
        >>> delete_response = await habitica.delete_task(task_id)
        >>> print(delete_response.success)  # True if successfully deleted
        """
        url = self.url / "api/v3/tasks" / str(task_id)

        return HabiticaResponse.from_json(
            await self._request("delete", url=url),
        )

    async def reorder_task(self, task_id: UUID, to: int) -> HabiticaTaskOrderResponse:
        """Reorder a user's tasks.

        This method sends a request to the Habitica API to reorder a specific task,
        identified by the given `task_id`, to a new position specified by `to`.

        Parameters
        ----------
        task_id : UUID
            The UUID of the task to reorder.
        to : int
            The new position to move the task to. Use 0 to move the task to the top,
            and -1 to move it to the bottom of the list.

        Returns
        -------
        HabiticaTaskOrderResponse
            A response object containing a list of task IDs in the new sort order.

        Raises
        ------
        aiohttp.ClientResponseError
            For HTTP-related errors, such as HTTP 400 or 500 response status.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        >>> task_id = UUID("12345678-1234-5678-1234-567812345678")
        >>> reorder_response = await habitica.reorder_task(task_id, 2)
        >>> print(reorder_response.data)  # Displays a list of task IDs in the new order
        """
        url = self.url / "api/v3/tasks" / str(task_id) / "move/to" / str(to)

        return HabiticaTaskOrderResponse.from_json(
            await self._request("post", url=url),
        )

    async def get_user_export(self) -> HabiticaUserExport:
        """Export the user's data from Habitica.

        Notes
        -----
        This endpoint is part of Habitica's private API and intended for use
        on the website only. It may change at any time without notice, and
        backward compatibility is not guaranteed.

        Returns
        -------
        HabiticaUserExportResponse:
            The user's exported data, containing
            information such as tasks, settings, and profile details.

        Raises
        ------
        NotAuthorizedError
            If the API request is unauthorized (HTTP 401).
        aiohttp.ClientResponseError
            For other HTTP-related errors raised by aiohttp, such as HTTP 400 or 500.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.
        """
        url = self.url / "export/userdata.json"

        return HabiticaUserExport.from_json(
            await self._request("get", url=url),
        )

    async def get_content(
        self,
        language: Language | None = None,
    ) -> HabiticaResponse:
        """
        Fetch game content from the Habitica API.

        This method retrieves the game content, which includes information
        such as available equipment, pets, mounts, and other game elements.

        Parameters
        ----------
        language : Language | None
            Optional language code to specify the localization of the content,
            possible values are defined in the `Language` enum.
            If not provided, it defaults to Language.EN or the authenticated
            user's language.

            Available languages include: BG, CS, DA, DE, EN, EN_PIRATE, EN_GB,
            ES, ES_419, FR, HE, HU, ID, IT, JA, NL, PL, PT, PT_BR, RO, RU, SK,
            SR, SV, UK, ZH, ZH_TW.


        Returns
        -------
        HabiticaResponse:
            A response object containing the game content in JSON format.

        Raises
        ------
        aiohttp.ClientResponseError
            For other HTTP-related errors raised by aiohttp, such as HTTP 400 or 500.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.
        """
        url = self.url / "api/v3/content"
        params = {}

        if language:
            params.update({"language": language.value})

        return HabiticaResponse.from_json(
            await self._request("get", url=url, params=params),
        )

    async def run_cron(self) -> HabiticaResponse:
        """Run the Habitica cron.

        This method triggers the cron process, which applies the daily reset for the authenticated user.
        It assumes that the user has already confirmed their activity for the previous day
        (i.e., checked off any Dailies they completed). The cron will immediately apply
        damage for incomplete Dailies that were due and handle other daily resets.

        Returns
        -------
        HabiticaResponse
            A response containing an empty data object.

        Raises
        ------
        NotAuthorizedError
            If the API request is unauthorized (HTTP 401).
        aiohttp.ClientResponseError
                For other HTTP-related errors raised by aiohttp, such as HTTP 400 or 500.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.
        """
        url = self.url / "api/v3/cron"
        return HabiticaResponse.from_json(await self._request("post", url=url))

    async def allocate_single_stat_point(
        self,
        stat: Attributes = Attributes.STR,
    ) -> HabiticaStatsResponse:
        """Allocate a single stat point to the specified attribute.

        If no stat is specified, the default is 'str' (strength).
        If the user does not have any stat points to allocate,
        a NotAuthorized error is returned.

        Parameters
        ----------
        stat : Attributes, optional
            The stat to increase, either 'str', 'con', 'int', or 'per'. Defaults to 'str'.

        Returns
        -------
        HabiticaAllocatStatPointsResponse
            A response containing the updated user stats, including points, buffs, and training data.

        Raises
        ------
        NotAuthorizedError
            If the user does not have enough stat points to allocate.
        aiohttp.ClientResponseError
                For other HTTP-related errors raised by aiohttp, such as HTTP 400 or 500.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        Allocate a single stat point to Intelligence:
        >>> await habitica.allocate_single_stat_point(stat=Attributes.INT)

        Allocate a single stat point to Strength (default):
        >>> await habitica.allocate_single_stat_point()
        """
        url = self.url / "api/v3/user/allocate"
        params = {"stat": stat}

        return HabiticaStatsResponse.from_json(
            await self._request("post", url=url, params=params),
        )

    async def allocate_stat_points(self) -> HabiticaStatsResponse:
        """Allocate all available stat points using the user's chosen automatic allocation method.

        This method uses the user's configured allocation strategy to distribute any unassigned
        stat points. If the user has no specific method defined, all points are allocated to
        Strength (STR). If there are no points to allocate, the method will still return a
        success response. The response includes updated user stats, including health, mana,
        experience, and gold.

        Returns
        -------
        HabiticaAllocatStatPointsResponse
            A response containing the updated user stats, including points, buffs, and training data.

        Raises
        ------
        NotAuthorizedError
            If the user does not have enough stat points to allocate.
        aiohttp.ClientResponseError
            For other HTTP-related errors raised by aiohttp, such as HTTP 400 or 500.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.
        """
        url = self.url / "api/v3/user/allocate-now"

        return HabiticaStatsResponse.from_json(
            await self._request("post", url=url),
        )

    async def allocate_bulk_stat_points(
        self,
        int_points: int = 0,
        str_points: int = 0,
        con_points: int = 0,
        per_points: int = 0,
    ) -> HabiticaStatsResponse:
        """Allocate multiple stat points manually to different attributes.

        This method allows the user to manually allocate their available stat points to the
        desired attributes. The number of points to allocate for each attribute must be provided
        as parameters. The request will fail if the user does not have enough available points.

        Parameters
        ----------
        int_points : int, optional
            The number of points to allocate to Intelligence (default is 0).
        str_points : int, optional
            The number of points to allocate to Strength (default is 0).
        con_points : int, optional
            The number of points to allocate to Constitution (default is 0).
        per_points : int, optional
            The number of points to allocate to Perception (default is 0).

        Returns
        -------
        HabiticaAllocatStatPointsResponse
            A response containing the updated user stats, including points, buffs, and training data.

        Raises
        ------
        NotAuthorizedError
            If the user does not have enough stat points to allocate.
        aiohttp.ClientResponseError
            For other HTTP-related errors raised by aiohttp, such as HTTP 400 or 500.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        Allocate 2 points to INT and 1 point to STR:
        >>> await allocate_bulk_stat_points(int_points=2, str_points=1)
        """
        url = self.url / "api/v3/user/allocate-bulk"
        json = {
            "stats": {
                "int": int_points,
                "str": str_points,
                "con": con_points,
                "per": per_points,
            },
        }

        return HabiticaStatsResponse.from_json(
            await self._request("post", url=url, json=json),
        )

    async def buy_health_potion(self) -> HabiticaStatsResponse:
        """Purchase a health potion for the authenticated user.

        If the user has enough gold and their health is not already full,
        this method allows them to buy a health potion to restore health.
        The user's current stats will be returned upon a successful purchase.

        Returns
        -------
        HabiticaStatResponse
            A response object containing the user's updated stats and a success message.

        Raises
        ------
        NotAuthorizedError
            If the user does not have enough gold or if the user's health is already at maximum.
        aiohttp.ClientResponseError
            For other HTTP-related errors raised by aiohttp, such as HTTP 400 or 500.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.
        """
        url = self.url / "api/v3/user/buy-health-potion"

        return HabiticaStatsResponse.from_json(
            await self._request("post", url=url),
        )

    async def cast_skill(
        self,
        spell: Skill,
        target_id: UUID | None = None,
    ) -> HabiticaUserResponse:
        """Cast a skill (spell) in Habitica, optionally targeting a specific user, task or party.

        Parameters
        ----------
        spell : Skill
            The skill (or spell) to be cast. This should be a valid `Skill` enum value.
        target_id : UUID, optional
            The unique identifier of the target for the skill. If the skill does not require a target,
            this can be omitted.

        Returns
        -------
        HabiticaStatResponse
            A response object containing the user's updated stats and a success message.

        Raises
        ------
        NotAuthorizedError
            If the user does not have enough mana.
        NotFoundError
            The specified task, party or user could not be found
        aiohttp.ClientResponseError
            For other HTTP-related errors raised by aiohttp, such as HTTP 400 or 500.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.
        """
        url = self.url / "api/v3/class/cast" / spell
        params = {}

        if target_id:
            params.update({"targetId": str(target_id)})
        return HabiticaUserResponse.from_json(
            await self._request("post", url=url, json=params),
        )

    async def toggle_sleep(
        self,
    ) -> HabiticaResponse:
        """Toggles the user's sleep mode in Habitica.

        Returns
        -------
        HabiticaResponse
            A response object containing the result of the sleep mode toggle,
            and the new sleep state (True if sleeping, False if not).

        Raises
        ------
        aiohttp.ClientResponseError
            For other HTTP-related errors raised by aiohttp, such as HTTP 400 or 500.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.
        """
        url = self.url / "api/v3/user/sleep"

        return HabiticaResponse.from_json(await self._request("post", url=url))

    async def revive(
        self,
    ) -> HabiticaResponse:
        """Revive user from death.

        Raises
        ------
        NotAuthorizedError
            If the player is not dead and therefore cannot be revived.
        aiohttp.ClientResponseError
            For other HTTP-related errors raised by aiohttp, such as HTTP 400 or 500.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.
        """
        url = self.url / "api/v3/user/revive"

        return HabiticaResponse.from_json(await self._request("post", url=url))

    async def change_class(self, Class: Class) -> HabiticaClassSystemResponse:  # noqa: N803
        """Change the user's class in Habitica.

        This method sends a request to the Habitica API to change the user's class
        (e.g., warrior, mage, rogue, healer) to the specified class.

        Parameters
        ----------
        Class : Class
            An instance of the `Class` enum representing the new class to assign to the user.

        Returns
        -------
        HabiticaClassSystemResponse
            A response object containing stats, flags, items and preferences.

        Raises
        ------
        NotAuthorizedError
            If the player cannot change class at this time (e.g., conditions not met).
        aiohttp.ClientResponseError
            For other HTTP-related errors raised by aiohttp, such as HTTP 400 or 500.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        >>> new_class = Class.WARRIOR
        >>> change_response = await habitica.change_class(new_class)
        >>> print(change_response.data.stats)  # Displays the user's stats after class change
        """
        url = self.url / "api/v3/user/change-class"
        params = {"class": Class.value}

        return HabiticaClassSystemResponse.from_json(
            await self._request("post", url=url, params=params)
        )

    async def disable_classes(self) -> HabiticaClassSystemResponse:
        """Disable the class system for the user in Habitica.

        This method sends a request to the Habitica API to disable the class system for the user.

        Returns
        -------
        HabiticaClassSystemResponse
            A response object containing stats, flags, and preferences.

        Raises
        ------
        aiohttp.ClientResponseError
            For other HTTP-related errors raised by aiohttp, such as HTTP 400 or 500.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        >>> disable_response = await habitica.disable_classes()
        >>> print(disable_response.data.stats)  # Displays the user's stats after disabling the class system
        """
        url = self.url / "api/v3/user/disable-classes"

        return HabiticaClassSystemResponse.from_json(
            await self._request("post", url=url)
        )

    async def delete_completed_todos(self) -> HabiticaResponse:
        """Delete all completed to-dos from the user's task list.

        This method sends a request to the Habitica API to delete all completed to-dos
        from the user's task list.

        Returns
        -------
        HabiticaResponse
            A response object containing an empty data object.

        Raises
        ------
        aiohttp.ClientResponseError
            For HTTP-related errors, such as HTTP 400 or 500 response status.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        >>> delete_response = await habitica.delete_completed_todos()
        >>> print(delete_response.success)  # True if successfully cleared completed to-dos
        """
        url = self.url / "api/v3/tasks/clearCompletedTodos"

        return HabiticaClassSystemResponse.from_json(
            await self._request("post", url=url)
        )

    async def update_score(
        self,
        task_id: UUID | str,
        direction: Direction,
    ) -> HabiticaScoreResponse:
        """Submit a score update for a task in Habitica.

        This method allows scoring a task based on its type:
        - For Dailies and To-Dos: Marks the task as complete or incomplete.
        - For Habits: Increases the positive or negative habit score.
        - For Rewards: Buys the reward

        Parameters
        ----------
        task_id : UUID | str
            The ID of the task or an alias (e.g., a slug) associated with the task.
        direction : Direction
            The direction to score the task, either `Direction.UP` to increase or complete the task,
            or `Direction.DOWN` to decrease or uncomplete it..

        Returns
        -------
        HabiticaScoreResponse
            A response object that contains the updated stats and item drop.

        Raises
        ------
        aiohttp.ClientResponseError
            For other HTTP-related errors raised by aiohttp, such as HTTP 400 or 500.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.
        """
        url = self.url / "api/v3/tasks" / str(task_id) / "score" / direction.value

        return HabiticaScoreResponse.from_json(
            await self._request("post", url=url),
        )

    async def get_tags(self) -> HabiticaTagsResponse:
        """Retrieve a user's tags from the Habitica API.

        This method sends a POST request to the Habitica API to fetch the tags
        associated with the user's account.

        Returns
        -------
        HabiticaTagsResponse
            A response object containing the user's tags.

        Raises
        ------
        aiohttp.ClientResponseError
            For other HTTP-related errors raised by aiohttp, such as HTTP 400 or 500.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        >>> tags_response = await habitica.get_tags()
        >>> print(tags_response.data)
        """
        url = self.url / "api/v3/tags"

        return HabiticaTagsResponse.from_json(
            await self._request("post", url=url),
        )

    async def get_tag(self, tag_id: UUID) -> HabiticaTagResponse:
        """Retrieve a specific tag from the Habitica API.

        This method sends a request to the Habitica API to retrieve a specific tag
        identified by the given `tag_id`.

        Parameters
        ----------
        tag_id : UUID
            The UUID of the tag to retrieve.

        Returns
        -------
        HabiticaTagResponse
            A response object containing the data for the specified tag.

        Raises
        ------
        aiohttp.ClientResponseError
            For other HTTP-related errors raised by aiohttp, such as HTTP 400 or 500.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        >>> tag_response = await habitica.get_tag()
        >>> print(tag_response.data)
        """
        url = self.url / "api/v3/tags" / str(tag_id)

        return HabiticaTagResponse.from_json(
            await self._request("post", url=url),
        )

    async def delete_tag(self, tag_id: UUID) -> HabiticaResponse:
        """Delete a user's tag from the Habitica API.

        This method sends a request to the Habitica API to delete a specific
        tag identified by the given `tag_id`.

        Parameters
        ----------
        tag_id : UUID
            The UUID of the tag to delete.

        Returns
        -------
        HabiticaTagResponse
            A response object with an empty data object.

        Raises
        ------
        aiohttp.ClientResponseError
            For HTTP-related errors, such as HTTP 400 or 500 response status.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        >>> tag_id = UUID("12345678-1234-5678-1234-567812345678")
        >>> delete_response = await habitica.delete_tag(tag_id)
        >>> print(delete_response.success)  # True if successfully deleted
        """
        url = self.url / "api/v3/tags" / str(tag_id)

        return HabiticaTagResponse.from_json(
            await self._request("delete", url=url),
        )

    async def create_tag(self, name: str) -> HabiticaTagResponse:
        """Create a new tag in the Habitica API.

        This method sends a request to the Habitica API to create a new tag
        with the specified `name`.

        Parameters
        ----------
        name : str
            The name to assign to the new tag.

        Returns
        -------
        HabiticaTagResponse
            A response object containing a dictionary with the newly
            created tag information, including the ID of the new tag.

        Raises
        ------
        aiohttp.ClientResponseError
            For HTTP-related errors, such as HTTP 400 or 500 response status.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        >>> new_tag_response = await habitica.create_tag("New Tag Name")
        >>> print(new_tag_response.data.id)  # Displays the id of the new tag
        """
        url = self.url / "api/v3/tags"
        json = {"name": name}
        return HabiticaTagResponse.from_json(
            await self._request("post", url=url, json=json),
        )

    async def update_tag(self, tag_id: UUID, name: str) -> HabiticaTagResponse:
        """Update a user's tag in the Habitica API.

        This method sends a request to the Habitica API to update the name of a
        specific tag, identified by the given `tag_id`.

        Parameters
        ----------
        tag_id : UUID
            The UUID of the tag to update.
        name : str
            The new name to assign to the tag.

        Returns
        -------
        HabiticaTagResponse
            A response object containing a dictionary with the updated tag information.

        Raises
        ------
        aiohttp.ClientResponseError
            For HTTP-related errors, such as HTTP 400 or 500 response status.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        >>> tag_id = UUID("12345678-1234-5678-1234-567812345678")
        >>> update_response = await habitica.update_tag(tag_id, "New Tag Name")
        >>> print(update_response.data)  # Displays the updated tag information
        """
        url = self.url / "api/v3/tags" / str(tag_id)
        json = {"name": name}
        return HabiticaTagResponse.from_json(
            await self._request("put", url=url, json=json),
        )

    async def reorder_tag(self, tag_id: UUID, to: int) -> HabiticaResponse:
        """Reorder a user's tag in the Habitica API.

        This method sends a request to the Habitica API to reorder a specific tag,
        identified by the given `tag_id`, to a new position specified by `to`.

        Parameters
        ----------
        tag_id : UUID
            The UUID of the tag to reorder.
        to : int
            The new position to move the tag to (starting from 0).

        Returns
        -------
        HabiticaResponse
            A response object containing an empty data object.

        Raises
        ------
        aiohttp.ClientResponseError
            For HTTP-related errors, such as HTTP 400 or 500 response status.
        aiohttp.ClientConnectionError
            If the connection to the API fails.
        aiohttp.ClientError
            For any other exceptions raised by aiohttp during the request.
        TimeoutError
            If the connection times out.

        Examples
        --------
        >>> tag_id = UUID("12345678-1234-5678-1234-567812345678")
        >>> reorder_response = await habitica.reorder_tag(tag_id, 2)
        >>> print(reorder_response.success)  # True if reorder is successful
        """
        url = self.url / "api/v3/reorder-tags"
        json = {"tagId": str(tag_id), "to": to}

        return HabiticaTagResponse.from_json(
            await self._request("post", url=url, json=json),
        )

    def _cache_asset(self, asset: str, asset_data: IO[bytes]) -> None:
        """Cache an asset and maintain the cache size limit by removing older entries.

        This method stores the given asset in the in-memory cache. If the cache exceeds the
        specified limit (`self._cache_size`), the oldest cached asset is removed.
        The cache is updated with the new asset, and its order of insertion is tracked.

        Parameters
        ----------
        asset : str
            The identifier or name of the asset to be cached.
        asset_data : IO[bytes]
            The asset data as an I/O stream of bytes to be cached.

        Notes
        -----
        If `self._cache_size` is zero or `None`, the caching operation is skipped. When
        the cache limit is exceeded, the least recently added asset is evicted to
        make space for the new asset.
        """
        if not self._cache_size:
            return
        if len(self._cache_order) > self._cache_size:
            del self._assets_cache[self._cache_order.pop(0)]
        self._assets_cache[asset] = asset_data
        self._cache_order.append(asset)

    async def paste_image(
        self,
        image: Image.Image,
        asset: str,
        position: tuple[int, int],
    ) -> None:
        """Fetch asset and paste it onto the base image at specified position.

        Parameters
        ----------
        image : Image
            The base image onto which the asset will be pasted.
        asset : str
            The name of the image asset to fetch (e.g., "hair_bangs_1_red.png").
            If no file extension is provided, `.png` will be added by default.
        position : tuple of int
            The (x, y) position coordinates where the asset will be pasted on the base image.

        Returns
        -------
        None
        """
        url = URL(ASSETS_URL) / f"{asset}"
        if not url.suffix:
            url = url.with_suffix(".png")
        try:
            if not (asset_data := self._assets_cache.get(asset)):
                async with self._session.get(url) as r:
                    r.raise_for_status()
                    asset_data = BytesIO(await r.read())
                    self._cache_asset(asset, asset_data)
        except ClientResponseError as e:
            _LOGGER.exception(
                "Failed to load %s.png due to error [%s]: %s",
                asset,
                e.status,
                e.message,
            )
        except ClientError:
            _LOGGER.exception(
                "Failed to load %s.png due to a request error",
                asset,
            )
        else:
            fetched_image = Image.open(asset_data).convert("RGBA")
            image.paste(fetched_image, position, fetched_image)

    async def generate_avatar(  # noqa: PLR0912, PLR0915
        self,
        fp: str | IO[bytes],
        user_styles: UserStyles | None = None,
        fmt: str | None = None,
    ) -> UserStyles:
        """Generate an avatar image based on the provided user styles or fetched user data.

        If no `user_styles` object is provided, the method retrieves user preferences, items, and stats
        for the authenticated user and builds the avatar accordingly. The base image is initialized
        as a transparent RGBA image of size (141, 147). A mount offset is applied based on the user's
        current mount status.

        Note:
            Animated avatars are not supported, animated gear and mounts will
            be pasted without animation, showing only the first sprite.


        Parameters
        ----------
        fp : str or IO[bytes]
            The file path or a bytes buffer to store or modify the avatar image.
        user_styles : UserStyles, optional
            The user style preferences, items, and stats. If not provided, the method will fetch
            this data.
        fmt : str
            If a file object is used instead of a filename, the format
            must be speciefied (e.g. "png").

        Returns
        -------
        UserStyles
            The user styles used to generate the avatar.

        Examples
        --------
        Using a bytes buffer:
        >>> avatar = BytesIO()
        >>> await habitica generate_avatar(avatar, fmt='png')

        Using a file path:
        >>> await habitica.generate_avatar("/path/to/image/avatar.png")
        """
        if not user_styles:
            user_styles = extract_user_styles(
                await self.get_user(user_fields=["preferences", "items", "stats"]),
            )
        preferences = user_styles.preferences
        items = user_styles.items
        stats = user_styles.stats
        mount_offset_y = 0 if items.currentMount else 24

        # Initializing the base image
        image = Image.new("RGBA", (141, 147), (255, 0, 0, 0))

        async def paste_gear(gear_type: str) -> None:
            """Fetch and paste gear from equipped or costume gear sets."""
            gear_set = (
                items.gear.costume if preferences.costume else items.gear.equipped
            )
            gear = getattr(gear_set, gear_type)
            if gear and gear != f"{gear_type}_base_0":
                # 2019 Kickstarter gear doesn't follow name conventions
                if special_ks2019 := BACKER_ONLY_GEAR.get(gear):
                    gear = special_ks2019
                # armor has slim and broad size options
                elif gear_type == "armor":
                    gear = f"{preferences.size}_{gear}"
                await self.paste_image(image, gear, (24, mount_offset_y))

        # fetch and paste the background
        if preferences.background:
            await self.paste_image(
                image,
                f"background_{preferences.background}",
                (0, 0),
            )

        # Fetch and paste the mount body
        if items.currentMount:
            await self.paste_image(
                image,
                f"Mount_Body_{items.currentMount}",
                (24, 18),
            )

        # Fetch and paste avatars for visual buffs
        if (
            stats.buffs.seafoam
            or stats.buffs.shinySeed
            or stats.buffs.snowball
            or stats.buffs.spookySparkles
        ):
            if stats.buffs.spookySparkles:
                await self.paste_image(image, "ghost", (24, mount_offset_y))
            if stats.buffs.shinySeed:
                await self.paste_image(
                    image,
                    f"avatar_snowball_{stats.Class}",
                    (24, mount_offset_y),
                )
            if stats.buffs.shinySeed:
                await self.paste_image(
                    image,
                    f"avatar_floral_{stats.Class}",
                    (24, mount_offset_y),
                )
            if stats.buffs.seafoam:
                await self.paste_image(
                    image,
                    "seafoam_star",
                    (24, mount_offset_y),
                )

            # Fetch and paste the hairflower
            if preferences.hair.flower:
                await self.paste_image(
                    image,
                    f"hair_flower_{preferences.hair.flower}",
                    (24, mount_offset_y),
                )

        else:
            # Fetch and paste the chair
            if preferences.chair and preferences.chair != "none":
                await self.paste_image(
                    image,
                    f"chair_{preferences.chair}",
                    (24, 0),
                )

            # Fetch and paste the back accessory
            await paste_gear("back")

            # Fetch and paste the skin
            await self.paste_image(
                image,
                f"skin_{preferences.skin}{"_sleep" if preferences.sleep else ""}",
                (24, mount_offset_y),
            )

            # Fetch and paste the shirt
            await self.paste_image(
                image,
                f"{preferences.size}_shirt_{preferences.shirt}",
                (24, mount_offset_y),
            )

            # Fetch and paste the head base
            await self.paste_image(image, "head_0", (24, mount_offset_y))

            # Fetch and paste the armor if not the base armor
            await paste_gear("armor")

            # Fetch and paste the hair elements
            for hair_type in ("bangs", "base", "mustache", "beard"):
                if style := getattr(preferences.hair, hair_type, 0):
                    await self.paste_image(
                        image,
                        f"hair_{hair_type}_{style}_{preferences.hair.color}",
                        (24, mount_offset_y),
                    )

            # Fetch and paste body accessory, eyewear, headgear and head accessory
            for gear in ("body", "eyewear", "head", "headAccessory"):
                await paste_gear(gear)

            # Fetch and paste the hairflower
            if preferences.hair.flower:
                await self.paste_image(
                    image,
                    f"hair_flower_{preferences.hair.flower}",
                    (24, mount_offset_y),
                )

            # Fetch and paste the shield
            await paste_gear("shield")
            # Fetch and paste the weapon
            await paste_gear("weapon")

        # Fetch and paste the zzz
        if preferences.sleep:
            await self.paste_image(image, "zzz", (24, mount_offset_y))

        # Fetch and paste the mount head
        if items.currentMount:
            await self.paste_image(
                image,
                f"Mount_Head_{items.currentMount}",
                (24, 18),
            )
        # Fetch and paste the pet
        if items.currentPet:
            await self.paste_image(image, f"Pet-{items.currentPet}", (0, 48))

        if isinstance(fp, str):
            loop = asyncio.get_running_loop()
            loop.run_in_executor(None, image.save, fp)
        else:
            image.save(fp, fmt)

        return user_styles
