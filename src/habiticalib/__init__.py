"""Modern asynchronous Python client library for the Habitica API."""

from .const import __version__
from .exceptions import HabiticaException, NotAuthorizedError, NotFoundError
from .lib import Habitica

__all__ = [
    "__version__",
    "Habitica",
    "HabiticaException",
    "NotAuthorizedError",
    "NotFoundError",
]
