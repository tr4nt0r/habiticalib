"""Helper functions for Habiticalib."""

from dataclasses import asdict
import platform
import uuid

import aiohttp

from .const import DEVELOPER_ID, __version__
from .types import HabiticaUserResponse, UserData, UserStyles


def join_fields(user_fields: list[str] | str) -> str:
    """Join user fields into a comma-separated string.

    This method takes a list of user fields or a single string and
    returns a string. If a list is provided, it joins the elements
    with a comma separator. If a string is provided, it returns
    the string as-is.

    Parameters
    ----------
    user_fields : list of str or str
        A list of user field strings or a single user field string.

    Returns
    -------
    str
        A comma-separated string of user fields if `user_fields` is a list,
        or the original string if `user_fields` is a single string.
    """
    return ",".join(user_fields) if isinstance(user_fields, list) else str(user_fields)


def get_user_agent() -> str:
    """Generate User-Agent string.

    The User-Agent string contains details about the operating system,
    its version, architecture, the habiticalib version, aiohttp version,
    and Python version.

    Returns
    -------
    str
        A User-Agent string with OS details, library versions, and a project URL.

    Examples
    --------
    >>> client.get_user_agent()
    'Habiticalib/0.0.0 (Windows 11 (10.0.22000); 64bit)
     aiohttp/3.10.9 Python/3.12.7  +https://github.com/tr4nt0r/habiticalib)'
    """
    os_name = platform.system()
    os_version = platform.version()
    os_release = platform.release()
    arch, _ = platform.architecture()
    os_info = f"{os_name} {os_release} ({os_version}); {arch}"

    return (
        f"Habiticalib/{__version__} ({os_info}) "
        f"aiohttp/{aiohttp.__version__} Python/{platform.python_version()} "
        " +https://github.com/tr4nt0r/habiticalib)"
    )


def get_x_client(x_client: str | None = None) -> str:
    """Generate the x-client header string.

    If a valid `x_client` is provided, it validates the User ID (UUID format).
    If no `x_client` is provided, it generates a default x-client header string.

    Parameters
    ----------
    x_client : str or None, optional
        A client identifier containing a UUID (first 36 characters) or None. If
        None, a default x-client header will be generated.

    Returns
    -------
    str
        The validated x-client header string or habiticalib's default x-client header.

    Raises
    ------
    ValueError
        If the provided `x_client` is not in a valid UUID format.

    Examples
    --------
    >>> get_x_client("123e4567-e89b-12d3-a456-426614174000 - MyHabiticaApp")
    '123e4567-e89b-12d3-a456-426614174000 - MyHabiticaApp'

    >>> get_x_client()
    '4c4ca53f-c059-4ffa-966e-9d29dd405daf - Habiticalib/0.0.0'
    """
    if x_client:
        try:
            uuid.UUID(x_client[:36])
        except ValueError as e:
            msg = (
                "Invalid User ID provided in x-client. Expected a valid "
                "UUID format. Please ensure the User ID is correct"
            )
            raise ValueError(msg) from e

        return x_client

    return f"{DEVELOPER_ID} - Habiticalib/{__version__}"


def extract_user_styles(user_data: HabiticaUserResponse) -> UserStyles:
    """Extract user styles from a user data object."""
    data: UserData = user_data.data
    return UserStyles.from_dict(asdict(data))
