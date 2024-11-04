"""Exceptions for Habiticalib."""

from datetime import datetime
from typing import Self

from multidict import CIMultiDictProxy

from habiticalib.types import HabiticaErrorResponse


class HabiticaException(Exception):  # noqa: N818
    """Base class for Habitica errors."""

    def __init__(
        self: Self,
        error: HabiticaErrorResponse,
        headers: CIMultiDictProxy,
    ) -> None:
        """Initialize the Exception."""
        self.error = error
        self.rate_limit: int | None = (
            int(r) if (r := headers.get("x-ratelimit-limit")) else None
        )
        self.rate_limit_remaining: int | None = (
            int(r) if (r := headers.get("x-ratelimit-remaining")) else None
        )
        self.rate_limit_reset: datetime | None = (
            datetime.strptime(r[:33], "%a %b %d %Y %H:%M:%S %Z%z")
            if (r := headers.get("x-ratelimit-reset"))
            else None
        )
        self.retry_after: int = round(float(headers.get("retry-after", 0)))

        super().__init__(error.message)


class NotAuthorizedError(HabiticaException):
    """NotAuthorized error."""


class NotFoundError(HabiticaException):
    """NotFound error."""


class BadRequestError(HabiticaException):
    """BadRequest error."""


class TooManyRequestsError(HabiticaException):
    """TooManyRequests error."""
