"""Exceptions for Habiticalib."""

from typing import Self

from habiticalib.types import HabiticaErrorResponse


class HabiticaException(Exception):  # noqa: N818
    """Base class for Habitica errors."""

    def __init__(self: Self, error: HabiticaErrorResponse) -> None:
        """Initialize the Exception."""
        self.error = error

        super().__init__(error.message)


class NotAuthorizedError(HabiticaException):
    """NotAuthorized error."""


class NotFoundError(HabiticaException):
    """NotFound error."""


class BadRequestError(HabiticaException):
    """BadRequest error."""
