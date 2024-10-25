"""Typedefs for Habiticalib."""

# pylint: disable=C0103
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum, StrEnum
from typing import Any
from uuid import UUID  # noqa: TCH003

from mashumaro import field_options
from mashumaro.config import BaseConfig
from mashumaro.mixins.orjson import DataClassORJSONMixin


def serialize_datetime(date: str | int | None) -> datetime | None:
    """Convert an iso date to a datetime.date object."""
    if isinstance(date, int):
        return datetime.fromtimestamp(date / 1000, tz=UTC)
    if isinstance(date, str):
        try:
            return datetime.fromisoformat(date)
        except ValueError:
            # sometimes nextDue dates are JavaScript datetime strings
            # instead of iso: "Mon May 06 2024 00:00:00 GMT+0200"
            # This was fixed in Habitica v5.28.9, nextDue dates are now isoformat
            try:
                return datetime.strptime(date, "%a %b %d %Y %H:%M:%S %Z%z")
            except ValueError:
                return None
    return None


@dataclass(kw_only=True)
class NotificationsUser:
    """Notifications User data."""

    Type: str = field(metadata=field_options(alias="type"))
    data: dict[str, Any]
    seen: bool
    id: UUID


@dataclass(kw_only=True)
class HabiticaResponse(DataClassORJSONMixin):
    """Representation of a base Habitica API response."""

    data: Any
    success: bool
    notifications: list[NotificationsUser] = field(default_factory=list)
    userV: int | None = None
    appVersion: str | None = None


@dataclass(kw_only=True)
class LoginData:
    """Login data."""

    id: UUID
    apiToken: str
    newUser: bool
    username: str


@dataclass(kw_only=True)
class HabiticaLoginResponse(HabiticaResponse):
    """Representation of a login data response."""

    data: LoginData


@dataclass(kw_only=True)
class LocalAuth:
    """Auth local data."""

    email: str
    username: str
    lowerCaseUsername: str
    has_password: bool


@dataclass(kw_only=True)
class LocalTimestamps:
    """Timestamps local data."""

    created: datetime
    loggedin: datetime
    updated: datetime


@dataclass(kw_only=True)
class AuthUser:
    """User auth data."""

    local: LocalAuth | None = None
    timestamps: LocalTimestamps | None = None
    facebook: dict | None = None
    google: dict | None = None
    apple: dict | None = None


@dataclass(kw_only=True)
class UltimateGearSetsAchievments:
    """Achievments ultimateGearSets data."""

    healer: bool | None = None
    wizard: bool | None = None
    rogue: bool | None = None
    warrior: bool | None = None


@dataclass(kw_only=True)
class QuestsAchievments:
    """Achievments quests."""

    bewilder: int | None = None
    burnout: int | None = None
    stressbeast: int | None = None
    harpy: int | None = None
    atom3: int | None = None
    vice3: int | None = None
    vice1: int | None = None
    gryphon: int | None = None
    evilsanta2: int | None = None
    evilsanta: int | None = None
    dilatory_derby: int | None = None
    dilatory: int | None = None
    atom2: int | None = None
    atom1: int | None = None
    dysheartener: int | None = None


@dataclass(kw_only=True)
class AchievementsUser:
    """User achievments data."""

    ultimateGearSets: UltimateGearSetsAchievments = field(
        default_factory=UltimateGearSetsAchievments
    )
    streak: int | None = None
    challenges: list = field(default_factory=list)
    perfect: int | None = None
    quests: QuestsAchievments = field(default_factory=QuestsAchievments)
    backToBasics: bool | None = None
    dustDevil: bool | None = None
    primedForPainting: bool | None = None
    completedTask: bool | None = None
    createdTask: bool | None = None
    fedPet: bool | None = None
    hatchedPet: bool | None = None
    purchasedEquipment: bool | None = None
    tickledPink: bool | None = None
    goodAsGold: bool | None = None
    boneCollector: bool | None = None
    seeingRed: bool | None = None
    violetsAreBlue: bool | None = None
    shadyCustomer: bool | None = None
    joinedGuild: bool | None = None
    joinedChallenge: bool | None = None
    partyUp: None = None


@dataclass(kw_only=True)
class BackerUser:
    """User backer data."""

    tier: int | None = None
    npc: str | None = None
    tokensApplied: bool | None = None


@dataclass(kw_only=True)
class PermissionsUser:
    """User permissions data."""

    fullAccess: bool | None = None
    news: bool | None = None
    userSupport: bool | None = None
    challengeAdmin: bool | None = None
    moderator: bool | None = None
    coupons: bool | None = None


@dataclass(kw_only=True)
class ContributorUser:
    """User contributer data."""

    contributions: str | None = None
    level: int | None = None
    text: str | None = None


@dataclass(kw_only=True)
class ConsecutivePlan:
    """Plan consecutive data."""

    trinkets: int | None = None
    gemCapExtra: int | None = None
    offset: int | None = None
    count: int | None = None


@dataclass(kw_only=True)
class PlanPurchased:
    """Purchased background data."""

    consecutive: ConsecutivePlan = field(default_factory=ConsecutivePlan)
    mysteryItems: list = field(default_factory=list)
    gemsBought: int | None = None
    extraMonths: int | None = None
    dateUpdated: datetime | None = None
    perkMonthCount: int | None = None
    quantity: int | None = None


@dataclass(kw_only=True)
class PurchasedUser:
    """User purchased data."""

    plan: PlanPurchased = field(default_factory=PlanPurchased)
    txnCount: int | None = None
    background: dict[str, bool] = field(default_factory=dict)
    shirt: dict[str, bool] = field(default_factory=dict)
    hair: dict[str, bool] = field(default_factory=dict)
    skin: dict[str, bool] = field(default_factory=dict)
    ads: bool | None = None
    mobileChat: bool | None = None


@dataclass(kw_only=True)
class TourFlags:
    """Flags tour data."""

    intro: int | None = None
    classes: int | None = None
    stats: int | None = None
    tavern: int | None = None
    party: int | None = None
    guilds: int | None = None
    challenges: int | None = None
    market: int | None = None
    pets: int | None = None
    mounts: int | None = None
    hall: int | None = None
    equipment: int | None = None
    groupPlans: int | None = None


@dataclass(kw_only=True)
class CommonTutorial:
    """Tutorial common data."""

    habits: bool
    dailies: bool
    todos: bool
    rewards: bool
    party: bool
    pets: bool
    gems: bool
    skills: bool
    classes: bool
    tavern: bool
    equipment: bool
    items: bool
    mounts: bool
    inbox: bool
    stats: bool


@dataclass(kw_only=True)
class IosTutorial:
    """Tutorial ios data."""

    addTask: bool
    editTask: bool
    deleteTask: bool
    filterTask: bool
    groupPets: bool
    inviteParty: bool
    reorderTask: bool


@dataclass(kw_only=True)
class TutorialFlags:
    """Flags tutorial data."""

    common: CommonTutorial | None = None
    ios: IosTutorial | None = None


@dataclass(kw_only=True)
class FlagsUser:
    """User flags data."""

    customizationsNotification: bool | None = None
    tour: TourFlags = field(default_factory=TourFlags)
    showTour: bool | None = None
    tutorial: TutorialFlags = field(default_factory=TutorialFlags)
    dropsEnabled: bool | None = None
    itemsEnabled: bool | None = None
    lastNewStuffRead: str | None = None
    rewrite: bool | None = None
    classSelected: bool | None = None
    rebirthEnabled: bool | None = None
    levelDrops: dict[str, bool] = field(default_factory=dict)
    recaptureEmailsPhase: int | None = None
    weeklyRecapEmailsPhase: int | None = None
    lastWeeklyRecap: datetime | None = None
    communityGuidelinesAccepted: bool | None = None
    cronCount: int | None = None
    welcomed: bool | None = None
    armoireEnabled: bool | None = None
    armoireOpened: bool | None = None
    armoireEmpty: bool | None = None
    cardReceived: bool | None = None
    warnedLowHealth: bool | None = None
    verifiedUsername: bool | None = None
    newStuff: bool | None = None
    thirdPartyTools: datetime | None = None
    mathUpdates: bool | None = None
    lastFreeRebirth: datetime | None = None
    chatRevoked: bool | None = None
    chatShadowMuted: bool | None = None
    lastWeeklyRecapDiscriminator: bool | None = None
    onboardingEmailsPhase: str | None = None


@dataclass(kw_only=True)
class EntryHistory:
    """History entry data."""

    date: datetime = field(
        metadata=field_options(
            deserialize=serialize_datetime,
        )
    )
    value: float
    scoredUp: int | None = None
    scoredDown: int | None = None
    isDue: bool | None = None
    completed: bool | None = None


@dataclass(kw_only=True)
class HistoryUser:
    """User history data."""

    todos: list[EntryHistory] = field(default_factory=list)
    exp: list[EntryHistory] = field(default_factory=list)


@dataclass(kw_only=True)
class EquippedGear:
    """Gear equipped data."""

    weapon: str | None = None
    armor: str | None = None
    head: str | None = None
    shield: str | None = None
    back: str | None = None
    headAccessory: str | None = None
    eyewear: str | None = None
    body: str | None = None


@dataclass(kw_only=True)
class GearItems:
    """Items gear data."""

    equipped: EquippedGear = field(default_factory=EquippedGear)
    costume: EquippedGear = field(default_factory=EquippedGear)
    owned: dict[str, bool] = field(default_factory=dict)


@dataclass(kw_only=True)
class SpecialItems:
    """Items special data."""

    birthdayReceived: list = field(default_factory=list)
    birthday: int | None = None
    thankyouReceived: list = field(default_factory=list)
    thankyou: int | None = None
    greetingReceived: list = field(default_factory=list)
    greeting: int | None = None
    nyeReceived: list = field(default_factory=list)
    nye: int | None = None
    valentineReceived: list = field(default_factory=list)
    valentine: int | None = None
    seafoam: int | None = None
    shinySeed: int | None = None
    spookySparkles: int | None = None
    snowball: int | None = None
    congrats: int | None = None
    congratsReceived: list = field(default_factory=list)
    getwell: int | None = None
    getwellReceived: list = field(default_factory=list)
    goodluck: int | None = None
    goodluckReceived: list = field(default_factory=list)


@dataclass(kw_only=True)
class LastDropItems:
    """LastDrop items data."""

    count: int | None = None
    date: datetime | None = None


@dataclass(kw_only=True)
class ItemsUser:
    """User items data."""

    gear: GearItems = field(default_factory=GearItems)
    special: SpecialItems = field(default_factory=SpecialItems)
    lastDrop: LastDropItems = field(default_factory=LastDropItems)
    currentMount: str | None = None
    currentPet: str | None = None
    quests: dict[str, int] = field(default_factory=dict)
    mounts: dict[str, bool] = field(default_factory=dict)
    food: dict[str, int] = field(default_factory=dict)
    hatchingPotions: dict[str, int] = field(default_factory=dict)
    eggs: dict[str, int] = field(default_factory=dict)
    pets: dict[str, int] = field(default_factory=dict)


@dataclass(kw_only=True)
class InvitationsUser:
    """Invitations user data."""

    party: dict = field(default_factory=dict)
    guilds: list = field(default_factory=list)
    parties: list = field(default_factory=list)


@dataclass(kw_only=True)
class ProgressQuest:
    """Quest progress data."""

    up: float | None = None
    down: float | None = None
    collect: dict = field(default_factory=dict)
    collectedItems: int | None = None


@dataclass(kw_only=True)
class QuestParty:
    """Party quest data."""

    progress: ProgressQuest = field(default_factory=ProgressQuest)
    RSVPNeeded: bool | None = None
    key: str | None = None
    completed: str | None = None


@dataclass(kw_only=True)
class PartyUser:
    """Party user data."""

    quest: QuestParty = field(default_factory=QuestParty)
    order: str | None = None
    orderAscending: str | None = None
    _id: UUID | None = None


@dataclass(kw_only=True)
class HairPreferences:
    """Hair preferences data."""

    color: str | None = None
    base: int | None = None
    bangs: int | None = None
    beard: int | None = None
    mustache: int | None = None
    flower: int | None = None


@dataclass(kw_only=True)
class EmailNotificationsPreferences:
    """EmailNotifications preferences data."""

    unsubscribeFromAll: bool | None = None
    newPM: bool | None = None
    kickedGroup: bool | None = None
    wonChallenge: bool | None = None
    giftedGems: bool | None = None
    giftedSubscription: bool | None = None
    invitedParty: bool | None = None
    invitedGuild: bool | None = None
    questStarted: bool | None = None
    invitedQuest: bool | None = None
    importantAnnouncements: bool | None = None
    weeklyRecaps: bool | None = None
    onboarding: bool | None = None
    majorUpdates: bool | None = None
    subscriptionReminders: bool | None = None
    contentRelease: bool | None = None


@dataclass(kw_only=True)
class PushNotificationsPreferences:
    """PushNotifications preferences data."""

    unsubscribeFromAll: bool | None = None
    newPM: bool | None = None
    wonChallenge: bool | None = None
    giftedGems: bool | None = None
    giftedSubscription: bool | None = None
    invitedParty: bool | None = None
    invitedGuild: bool | None = None
    questStarted: bool | None = None
    invitedQuest: bool | None = None
    majorUpdates: bool | None = None
    mentionParty: bool | None = None
    mentionJoinedGuild: bool | None = None
    mentionUnjoinedGuild: bool | None = None
    partyActivity: bool | None = None
    contentRelease: bool | None = None


@dataclass(kw_only=True)
class SuppressModalsPreferences:
    """SupressModals preferences data."""

    levelUp: bool | None = None
    hatchPet: bool | None = None
    raisePet: bool | None = None
    streak: bool | None = None


@dataclass(kw_only=True)
class ActiveFilterTask:
    """ActiveFilter task data."""

    habit: str | None = None
    daily: str | None = None
    todo: str | None = None
    reward: str | None = None


@dataclass(kw_only=True)
class TasksPreferences:
    """Tasks preferences data."""

    activeFilter: ActiveFilterTask = field(default_factory=ActiveFilterTask)
    groupByChallenge: bool | None = None
    confirmScoreNotes: bool | None = None
    mirrorGroupTasks: list[UUID] = field(default_factory=list)


@dataclass(kw_only=True)
class PreferencesUser:
    """Preferences user data."""

    hair: HairPreferences = field(default_factory=HairPreferences)
    emailNotifications: EmailNotificationsPreferences = field(
        default_factory=EmailNotificationsPreferences
    )
    pushNotifications: PushNotificationsPreferences = field(
        default_factory=PushNotificationsPreferences
    )
    suppressModals: SuppressModalsPreferences = field(
        default_factory=SuppressModalsPreferences
    )
    tasks: TasksPreferences = field(default_factory=TasksPreferences)
    dayStart: int | None = None
    size: str | None = None
    hideHeader: bool | None = None
    skin: str | None = None
    shirt: str | None = None
    timezoneOffset: int | None = None
    sound: str | None = None
    chair: str | None = None
    allocationMode: str | None = None
    autoEquip: bool | None = None
    costume: bool | None = None
    dateFormat: str | None = None
    sleep: bool | None = None
    stickyHeader: bool | None = None
    disableClasses: bool | None = None
    newTaskEdit: bool | None = None
    dailyDueDefaultView: bool | None = None
    advancedCollapsed: bool | None = None
    toolbarCollapsed: bool | None = None
    reverseChatOrder: bool | None = None
    developerMode: bool | None = None
    displayInviteToPartyWhenPartyIs1: bool | None = None
    background: str | None = None
    automaticAllocation: bool | None = None
    webhooks: dict = field(default_factory=dict)
    improvementCategories: list[str] = field(default_factory=list)
    timezoneOffsetAtLastCron: int | None = None
    language: str | None = None


@dataclass(kw_only=True)
class ProfileUser:
    """Profile user data."""

    blurb: str | None = None
    imageUrl: str | None = None
    name: str | None = None


@dataclass(kw_only=True)
class BuffsStats:
    """Buffs stats data."""

    Str: int | None = field(default=None, metadata=field_options(alias="str"))
    per: int | None = None
    con: int | None = None
    stealth: int | None = None
    streaks: bool | None = None
    seafoam: bool | None = None
    shinySeed: bool | None = None
    snowball: bool | None = None
    spookySparkles: bool | None = None
    Int: int | None = field(default=None, metadata=field_options(alias="int"))


@dataclass(kw_only=True)
class TrainingStats:
    """Training stats data."""

    Str: float | None = field(default=None, metadata=field_options(alias="str"))
    per: int | None = None
    con: int | None = None
    Int: int | None = field(default=None, metadata=field_options(alias="int"))


@dataclass(kw_only=True)
class StatsUser:
    """Stats user data."""

    buffs: BuffsStats = field(default_factory=BuffsStats)
    training: TrainingStats = field(default_factory=TrainingStats)
    hp: float | None = None
    mp: float | None = None
    exp: int | None = None
    gp: float | None = None
    lvl: int | None = None
    Class: str = field(default="warrior", metadata=field_options(alias="class"))
    points: int | None = None
    Str: int | None = field(default=None, metadata=field_options(alias="str"))
    con: int | None = None
    per: int | None = None
    toNextLevel: int | None = None
    maxHealth: int | None = None
    maxMP: int | None = None
    Int: int | None = field(default=None, metadata=field_options(alias="int"))


@dataclass(kw_only=True)
class TagsUser:
    """Tags user data."""

    id: UUID | None = None
    name: str | None = None
    challenge: bool | None = None
    group: str | None = None


@dataclass(kw_only=True)
class InboxUser:
    """Inbox user data."""

    newMessages: int | None = None
    optOut: bool | None = None
    blocks: list = field(default_factory=list)
    messages: dict = field(default_factory=dict)


@dataclass(kw_only=True)
class TasksOrderUser:
    """TasksOrder user data."""

    habits: list[str] = field(default_factory=list)
    dailys: list[str] = field(default_factory=list)
    todos: list[str] = field(default_factory=list)
    rewards: list[str] = field(default_factory=list)


@dataclass(kw_only=True)
class PushDevicesUser:
    """PushDevices user data."""

    regId: str
    Type: str = field(metadata=field_options(alias="type"))
    createdAt: datetime
    updatedAt: datetime


@dataclass(kw_only=True)
class WebhooksUser:
    """Webhooks user data."""

    id: UUID
    Type: str = field(metadata=field_options(alias="type"))
    label: str
    url: str
    enabled: bool
    failures: int
    lastFailureAt: datetime | None


@dataclass(kw_only=True)
class PinnedItemsUser:
    """PinnedItems user data."""

    path: str
    Type: str = field(metadata=field_options(alias="type"))


@dataclass(kw_only=True)
class UserData:
    """User data."""

    id: UUID | None = None
    preferences: PreferencesUser = field(default_factory=PreferencesUser)
    flags: FlagsUser | None = None
    auth: AuthUser = field(default_factory=AuthUser)
    achievements: AchievementsUser = field(default_factory=AchievementsUser)
    backer: BackerUser = field(default_factory=BackerUser)
    contributor: ContributorUser = field(default_factory=ContributorUser)
    permissions: PermissionsUser = field(default_factory=PermissionsUser)
    purchased: PurchasedUser = field(default_factory=PurchasedUser)
    history: HistoryUser = field(default_factory=HistoryUser)
    items: ItemsUser = field(default_factory=ItemsUser)
    invitations: InvitationsUser = field(default_factory=InvitationsUser)
    party: PartyUser = field(default_factory=PartyUser)
    profile: ProfileUser = field(default_factory=ProfileUser)
    stats: StatsUser = field(default_factory=StatsUser)
    notifications: list[NotificationsUser] = field(default_factory=list)
    tags: list[TagsUser] = field(default_factory=list)
    inbox: InboxUser = field(default_factory=InboxUser)
    tasksOrder: TasksOrderUser = field(default_factory=TasksOrderUser)
    extra: dict = field(default_factory=dict)
    pushDevices: list[PushDevicesUser] = field(default_factory=list)
    webhooks: list[WebhooksUser] = field(default_factory=list)
    loginIncentives: int | None = None
    invitesSent: int | None = None
    pinnedItems: list[PinnedItemsUser] = field(default_factory=list)
    pinnedItemsOrder: list[str] = field(default_factory=list)
    unpinnedItems: list[PinnedItemsUser] = field(default_factory=list)
    secret: str | None = None
    balance: float | None = None
    lastCron: datetime | None = None
    needsCron: bool | None = None
    challenges: list[str] = field(default_factory=list)
    guilds: list[str] = field(default_factory=list)
    newMessages: dict[str, bool] = field(default_factory=dict)


@dataclass(kw_only=True)
class HabiticaUserResponse(HabiticaResponse):
    """Representation of a user data response."""

    data: UserData


@dataclass(kw_only=True)
class CompletedBy:
    """Task group completedby data."""

    userId: UUID | None = None
    date: datetime | None = None


@dataclass(kw_only=True)
class GroupTask:
    """Task group data."""

    assignedUsers: list[UUID] | None = None
    id: UUID | None = None
    assignedDate: datetime | None = None
    assigningUsername: str | None = None
    assignedUsersDetail: dict[str, Any] = field(default_factory=dict)
    taskId: UUID | None = None
    managerNotes: str | None = None
    completedBy: CompletedBy = field(default_factory=CompletedBy)


@dataclass(kw_only=True)
class Repeat:
    """Task repeat data."""

    m: bool = True
    t: bool = True
    w: bool = True
    th: bool = False
    f: bool = False
    s: bool = False
    su: bool = False


class ChallengeAbortedReason(StrEnum):
    """Task challenge aborted reason data."""

    CHALLENGE_DELETED = "CHALLENGE_DELETED"
    TASK_DELETED = "TASK_DELETED"
    UNSUBSCRIBED = "UNSUBSCRIBED"
    CHALLENGE_CLOSED = "CHALLENGE_CLOSED"
    CHALLENGE_TASK_NOT_FOUND = "CHALLENGE_TASK_NOT_FOUND"


@dataclass(kw_only=True)
class Challenge:
    """Challenge task data."""

    id: UUID | None = None
    taskId: UUID | None = None
    shortName: str | None = None
    broken: ChallengeAbortedReason | None = None
    winner: str | None = None


@dataclass(kw_only=True)
class Reminders:
    """Task reminders data."""

    id: UUID
    time: datetime
    startDate: datetime | None = None


class TaskType(StrEnum):
    """Task types enum."""

    DAILY = "daily"
    TODO = "todo"
    HABIT = "habit"
    REWARD = "reward"


class Attributes(StrEnum):
    """Character attributes enum."""

    STR = "str"
    CON = "con"
    INT = "int"
    PER = "per"


class Frequency(StrEnum):
    """Recurrence frequency enum."""

    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    YEARLY = "yearly"


@dataclass(kw_only=True)
class Task(DataClassORJSONMixin):
    """Representation of a task."""

    class Config(BaseConfig):
        """Config."""

        omit_none = True

    text: str | None = None
    attribute: Attributes | None = None
    alias: str | None = None
    notes: str | None = None
    tags: list[UUID] | None = None
    collapseChecklist: bool | None = None
    date: datetime | None = None
    priority: TaskPriority | None = None
    reminders: list[Reminders] | None = None
    checklist: list[str] | None = None
    Type: TaskType | None = field(default=None, metadata=field_options(alias="type"))
    up: bool | None = None
    down: bool | None = None
    counterUp: int | None = None
    counterDown: int | None = None
    startDate: datetime | None = None
    frequency: Frequency | None = None
    everyX: int | None = None
    repeat: Repeat | None = None
    daysOfMonth: list[int] | None = None
    weeksOfMonth: list[int] | None = None
    completed: bool | None = None
    streak: int | None = None


@dataclass(kw_only=True)
class TaskData:
    """Task data."""

    challenge: Challenge = field(default_factory=Challenge)
    group: GroupTask = field(default_factory=GroupTask)
    Type: TaskType | None = field(default=None, metadata=field_options(alias="type"))
    text: str | None = None
    notes: str | None = None
    tags: list[UUID] | None = None
    value: float | None = None
    priority: TaskPriority | None = None
    attribute: Attributes | None = None
    byHabitica: bool | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None
    date: datetime | None = None
    id: UUID | None = None
    userId: UUID | None = None
    up: bool | None = None
    down: bool | None = None
    counterUp: int | None = None
    counterDown: int | None = None
    frequency: Frequency | None = None
    history: list[EntryHistory] | None = None
    alias: str | None = None
    everyX: int | None = None
    startDate: datetime | None = None
    streak: int | None = None
    reminders: list[Reminders] = field(default_factory=list)
    daysOfMonth: list[int] = field(default_factory=list)
    weeksOfMonth: list[int] = field(default_factory=list)
    nextDue: list[datetime] = field(
        default_factory=list,
        metadata=field_options(deserialize=lambda x: list(map(serialize_datetime, x))),
    )
    yesterDaily: bool | None = None
    completed: bool | None = None
    collapseChecklist: bool = False
    checklist: list[str] = field(default_factory=list)
    isDue: bool | None = None
    repeat: Repeat = field(default_factory=Repeat)


@dataclass(kw_only=True)
class HabiticaTasksResponse(HabiticaResponse):
    """Repesentation of a tasks data response."""

    data: list[TaskData]


@dataclass(kw_only=True)
class HabiticaTaskResponse(HabiticaResponse):
    """Repesentation of a single task data response."""

    data: TaskData


@dataclass(kw_only=True)
class HabiticaErrorResponse(DataClassORJSONMixin):
    """Base class for Habitica errors."""

    success: bool
    error: str
    message: str


@dataclass(kw_only=True)
class TasksUserExport:
    """Tasks user export data."""

    todos: list[TaskData] = field(default_factory=list)
    dailys: list[TaskData] = field(default_factory=list)
    habits: list[TaskData] = field(default_factory=list)
    rewards: list[TaskData] = field(default_factory=list)


@dataclass(kw_only=True)
class BuffsUserStyles:
    """Buffs UserStyles data."""

    per: int | None = None
    con: int | None = None
    stealth: int | None = None
    seafoam: bool | None = None
    shinySeed: bool | None = None
    snowball: bool | None = None
    spookySparkles: bool | None = None


@dataclass(kw_only=True)
class StatsUserStyles:
    """Stats user styles data."""

    buffs: BuffsUserStyles = field(default_factory=BuffsUserStyles)
    Class: str = field(default="warrior", metadata=field_options(alias="class"))


@dataclass(kw_only=True)
class GearItemsUserStyles:
    """Items gear data."""

    equipped: EquippedGear = field(default_factory=EquippedGear)
    costume: EquippedGear = field(default_factory=EquippedGear)


@dataclass(kw_only=True)
class ItemsUserStyles:
    """Items user styles data."""

    gear: GearItemsUserStyles = field(default_factory=GearItemsUserStyles)
    currentMount: str | None = None
    currentPet: str | None = None


@dataclass(kw_only=True)
class PreferencesUserStyles:
    """Preferences user styles data."""

    hair: HairPreferences = field(default_factory=HairPreferences)
    size: str | None = None
    skin: str | None = None
    shirt: str | None = None
    chair: str | None = None
    costume: bool | None = None
    sleep: bool | None = None
    background: str | None = None


@dataclass(kw_only=True)
class UserStyles(DataClassORJSONMixin):
    """Represents minimalistic data only containing user styles."""

    items: ItemsUserStyles = field(default_factory=ItemsUserStyles)
    preferences: PreferencesUserStyles = field(default_factory=PreferencesUserStyles)
    stats: StatsUserStyles = field(default_factory=StatsUserStyles)


@dataclass(kw_only=True)
class HabiticaUserExport(UserData, DataClassORJSONMixin):
    """Representation of a user data export."""

    tasks: TasksUserExport = field(default_factory=TasksUserExport)


@dataclass(kw_only=True)
class HabiticaStatsResponse(HabiticaResponse):
    """Representation of a response containing stats data."""

    data: StatsUser


@dataclass(kw_only=True)
class QuestTmpScore:
    """Represents the quest progress details."""

    progressDelta: float | None = None
    collection: int | None = None


@dataclass(kw_only=True)
class DropTmpScore:
    """Represents the details of an item drop."""

    target: str | None = None
    canDrop: bool | None = None
    value: int | None = None
    key: str | None = None
    type: str | None = None
    dialog: str | None = None


@dataclass(kw_only=True)
class TmpScore:
    """Temporary quest and drop data."""

    quest: QuestTmpScore = field(default_factory=QuestTmpScore)
    drop: DropTmpScore = field(default_factory=DropTmpScore)


@dataclass(kw_only=True)
class HabiticaScoreResponse(StatsUser, DataClassORJSONMixin):
    """Representation of a score response."""

    delta: float | None = None
    _tmp: TmpScore = field(default_factory=TmpScore)


@dataclass(kw_only=True)
class HabiticaTagsResponse(HabiticaResponse, DataClassORJSONMixin):
    """Representation of a score response."""

    data: list[TagsUser]


@dataclass(kw_only=True)
class HabiticaTagResponse(HabiticaResponse, DataClassORJSONMixin):
    """Representation of a score response."""

    data: TagsUser


@dataclass
class ChangeClassData:
    """Change class data."""

    preferences: PreferencesUser = field(default_factory=PreferencesUser)
    flags: FlagsUser = field(default_factory=FlagsUser)
    items: ItemsUser = field(default_factory=ItemsUser)
    stats: StatsUser = field(default_factory=StatsUser)


@dataclass(kw_only=True)
class HabiticaClassSystemResponse(HabiticaResponse, DataClassORJSONMixin):
    """Representation of a change-class response."""

    data: ChangeClassData


@dataclass
class HabiticaTaskOrderResponse(HabiticaResponse):
    """Representation of a reorder task response."""

    data: TasksOrderUser = field(default_factory=TasksOrderUser)


class TaskFilter(StrEnum):
    """Enum representing the valid types of tasks for requests."""

    HABITS = "habits"
    DAILYS = "dailys"
    TODOS = "todos"
    REWARDS = "rewards"
    COMPLETED_TODOS = "completedTodos"


class Language(StrEnum):
    """Valid languages for Habitica content."""

    BG = "bg"
    CS = "cs"
    DA = "da"
    DE = "de"
    EN = "en"
    EN_PIRATE = "en@pirate"
    EN_GB = "en_GB"
    ES = "es"
    ES_419 = "es_419"
    FR = "fr"
    HE = "he"
    HU = "hu"
    ID = "id"
    IT = "it"
    JA = "ja"
    NL = "nl"
    PL = "pl"
    PT = "pt"
    PT_BR = "pt_BR"
    RO = "ro"
    RU = "ru"
    SK = "sk"
    SR = "sr"
    SV = "sv"
    UK = "uk"
    ZH = "zh"
    ZH_TW = "zh_TW"


class Skill(StrEnum):
    """Skills or spells available for casting."""

    # Mage skills
    BURST_OF_FLAMES = "fireball"
    ETHEREAL_SURGE = "mpheal"
    EARTHQUAKE = "earth"
    CHILLING_FROST = "frost"
    # Warrior skills
    BRUTAL_SMASH = "smash"
    DEFENSIVE_STANCE = "defensiveStance"
    VALOROUS_PRESENCE = "valorousPresence"
    INTIMIDATING_GAZE = "intimidate"
    # Rogue skills
    PICKPOCKET = "Pickpocket"
    BACKSTAB = "backStab"
    TOOLS_OF_THE_TRADE = "toolsOfTrade"
    STEALTH = "stealth"
    # Healer skills
    HEALING_LIGHT = "heal"
    PROTECTIVE_AURA = "protectAura"
    SEARING_BRIGHTNESS = "brightness"
    BLESSING = "healAll"
    # Transformation buffs
    SNOWBALL = "snowball"
    SPOOKY_SPARKLES = "spookySparkles"
    SEAFOAM = "seafoam"
    SHINY_SEED = "shinySeed"
    # Debuff potions
    SALT = "salt"  # removes snowball buff
    OPAQUE_POTION = "opaquePotion"  # removes spooky sparkles buff
    SAND = "sand"  # removes seafoam buff
    PETAL_FREE_POTION = "petalFreePotion"


class Class(StrEnum):
    """Habitica's player classes."""

    WARRIOR = "warrior"
    ROGUE = "rogue"
    MAGE = "mage"
    HEALER = "healer"


class Direction(StrEnum):
    """Direction to score a task."""

    UP = "up"
    DOWN = "down"


class TaskPriority(Enum):
    """Task difficulties."""

    TRIVIAL = 0.1
    EASY = 1
    MEDIUM = 1.5
    HARD = 2
