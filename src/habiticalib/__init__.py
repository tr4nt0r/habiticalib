"""Modern asynchronous Python client library for the Habitica API."""

from .const import ASSETS_URL, DEFAULT_URL, __version__
from .exceptions import (
    BadRequestError,
    HabiticaException,
    NotAuthorizedError,
    NotFoundError,
    TooManyRequestsError,
)
from .helpers import deserialize_task
from .lib import Habitica
from .types import (
    Attributes,
    ChangeClassData,
    ContentData,
    Direction,
    Frequency,
    HabiticaClass,
    HabiticaClassSystemResponse,
    HabiticaContentResponse,
    HabiticaErrorResponse,
    HabiticaGroupMembersResponse,
    HabiticaLoginResponse,
    HabiticaQuestResponse,
    HabiticaResponse,
    HabiticaScoreResponse,
    HabiticaSleepResponse,
    HabiticaStatsResponse,
    HabiticaTagResponse,
    HabiticaTagsResponse,
    HabiticaTaskOrderResponse,
    HabiticaTaskResponse,
    HabiticaTasksResponse,
    HabiticaUserAnonymized,
    HabiticaUserExport,
    HabiticaUserResponse,
    Language,
    LoginData,
    QuestData,
    ScoreData,
    Skill,
    StatsUser,
    TagsUser,
    Task,
    TaskData,
    TaskFilter,
    TaskPriority,
    TaskType,
    UserAnonymizedData,
    UserData,
    UserStyles,
)

__all__ = [
    "ASSETS_URL",
    "DEFAULT_URL",
    "Attributes",
    "BadRequestError",
    "ChangeClassData",
    "ContentData",
    "Direction",
    "Frequency",
    "Habitica",
    "HabiticaClass",
    "HabiticaClassSystemResponse",
    "HabiticaContentResponse",
    "HabiticaErrorResponse",
    "HabiticaException",
    "HabiticaGroupMembersResponse",
    "HabiticaLoginResponse",
    "HabiticaQuestResponse",
    "HabiticaResponse",
    "HabiticaScoreResponse",
    "HabiticaSleepResponse",
    "HabiticaStatsResponse",
    "HabiticaTagResponse",
    "HabiticaTagsResponse",
    "HabiticaTaskOrderResponse",
    "HabiticaTaskResponse",
    "HabiticaTasksResponse",
    "HabiticaUserAnonymized",
    "HabiticaUserExport",
    "HabiticaUserResponse",
    "Language",
    "LoginData",
    "NotAuthorizedError",
    "NotFoundError",
    "QuestData",
    "ScoreData",
    "Skill",
    "StatsUser",
    "TagsUser",
    "Task",
    "TaskData",
    "TaskFilter",
    "TaskPriority",
    "TaskType",
    "TooManyRequestsError",
    "UserAnonymizedData",
    "UserData",
    "UserStyles",
    "__version__",
    "deserialize_task",
]
