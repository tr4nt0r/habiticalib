"""Modern asynchronous Python client library for the Habitica API."""

from .exceptions import HabiticaException, NotAuthorizedError, NotFoundError
from .lib import Habitica

__version__ = "0.0.0"
__all__ = [
    "Habitica",
    "HabiticaException",
    "NotAuthorizedError",
    "NotFoundError",
]
