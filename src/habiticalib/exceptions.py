"""Exceptions for Habiticalib."""

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
        self.rate_limit = headers.get("x-ratelimit-limit")
        self.rate_limit_remaining = headers.get("x-ratelimit-remaining")
        self.rate_limit_reset = headers.get("x-ratelimit-reset")
        self.retry_after = headers.get("retry-after")

        super().__init__(error.message)


class NotAuthorizedError(HabiticaException):
    """NotAuthorized error."""


class NotFoundError(HabiticaException):
    """NotFound error."""


class BadRequestError(HabiticaException):
    """BadRequest error."""


class TooManyRequestsError(HabiticaException):
    """TooManyRequests error."""
