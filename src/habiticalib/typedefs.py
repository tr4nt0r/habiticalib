"""Typedefs for Habiticalib."""

# pylint: disable=C0103
from __future__ import annotations

from dataclasses import dataclass, field
import datetime as dt
from datetime import UTC, datetime
from enum import Enum, StrEnum
from typing import Annotated, Any, NotRequired, TypedDict
from uuid import UUID

from mashumaro import field_options
from mashumaro.config import TO_DICT_ADD_OMIT_NONE_FLAG
from mashumaro.mixins.orjson import DataClassORJSONMixin
from mashumaro.types import Discriminator


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


@dataclass
class BaseModel(DataClassORJSONMixin):
    """Base config for dataclasses."""

    class Config:
        """Configuration for TaskData."""

        aliases = {  # noqa: RUF012
            "Type": "type",
            "Str": "str",
            "Int": "int",
            "Class": "class",
            "tmp": "_tmp",
            "Def": "def",
            "Set": "set",
        }
        serialize_by_alias = True
        omit_none = True
        code_generation_options = [TO_DICT_ADD_OMIT_NONE_FLAG]  # noqa: RUF012

    def __eq__(self, value: object) -> bool:
        """Check if two instances are equal."""
        if issubclass(type(value), type(self)):
            return all(
                getattr(self, field) == getattr(value, field)
                for field in self.__dataclass_fields__
            )
        return super().__eq__(value)


@dataclass(kw_only=True)
class EquippedGear(BaseModel):
    """Gear equipped data."""

    weapon: str | None = None
    armor: str | None = None
    head: str | None = None
    shield: str | None = None
    back: str | None = None
    headAccessory: str | None = None
    eyewear: str | None = None
    body: str | None = None


@dataclass(kw_only=True, eq=False)
class GearItemsAvatar(BaseModel):
    """Items gear avatar data."""

    equipped: EquippedGear = field(default_factory=EquippedGear)
    costume: EquippedGear = field(default_factory=EquippedGear)


@dataclass(kw_only=True, eq=False)
class ItemsAvatar(BaseModel):
    """Items avatar data."""

    gear: GearItemsAvatar = field(default_factory=GearItemsAvatar)
    currentMount: str | None = None
    currentPet: str | None = None


class HabiticaClass(StrEnum):
    """Habitica's player classes."""

    WARRIOR = "warrior"
    ROGUE = "rogue"
    MAGE = "wizard"
    HEALER = "healer"


@dataclass(kw_only=True)
class HairPreferences(BaseModel):
    """Hair preferences data."""

    color: str | None = None
    base: int | None = None
    bangs: int | None = None
    beard: int | None = None
    mustache: int | None = None
    flower: int | None = None


@dataclass(kw_only=True, eq=False)
class PreferencesAvatar(BaseModel):
    """Preferences avatar data."""

    hair: HairPreferences = field(default_factory=HairPreferences)
    size: str | None = None
    skin: str | None = None
    shirt: str | None = None
    chair: str | None = None
    costume: bool | None = None
    sleep: bool | None = None
    background: str | None = None


@dataclass(kw_only=True, eq=False)
class BuffsStatsavatar(BaseModel):
    """Buffs stats avatar data."""

    seafoam: bool | None = None
    shinySeed: bool | None = None
    snowball: bool | None = None
    spookySparkles: bool | None = None


@dataclass(kw_only=True, eq=False)
class StatsAvatar(BaseModel):
    """Stats avatar data."""

    buffs: BuffsStatsavatar = field(default_factory=BuffsStatsavatar)
    Class: HabiticaClass = HabiticaClass.WARRIOR


@dataclass(kw_only=True, eq=False)
class Avatar(BaseModel):
    """Represents data for avatar visuals."""

    items: ItemsAvatar = field(default_factory=ItemsAvatar)
    preferences: PreferencesAvatar = field(default_factory=PreferencesAvatar)
    stats: StatsAvatar = field(default_factory=StatsAvatar)


@dataclass(kw_only=True)
class NotificationsUser(BaseModel):
    """Notifications User data."""

    Type: str
    data: dict[str, Any]
    seen: bool
    id: UUID


@dataclass(kw_only=True)
class HabiticaResponse(BaseModel):
    """Representation of a base Habitica API response."""

    data: Any
    success: bool
    notifications: list[NotificationsUser] = field(default_factory=list)
    userV: int | None = None
    appVersion: str | None = None


@dataclass(kw_only=True)
class LoginData(BaseModel):
    """Login data."""

    id: UUID
    apiToken: str
    newUser: bool
    username: str
    passwordResetCode: str | None = None


@dataclass(kw_only=True)
class HabiticaLoginResponse(HabiticaResponse):
    """Representation of a login data response."""

    data: LoginData


@dataclass(kw_only=True)
class LocalAuth(BaseModel):
    """Auth local data."""

    email: str | None = None
    username: str | None = None
    lowerCaseUsername: str | None = None
    has_password: bool | None = None


@dataclass(kw_only=True)
class LocalTimestamps(BaseModel):
    """Timestamps local data."""

    created: datetime | None = None
    loggedin: datetime | None = None
    updated: datetime | None = None


@dataclass(kw_only=True)
class AuthUser(BaseModel):
    """User auth data."""

    local: LocalAuth = field(default_factory=LocalAuth)
    timestamps: LocalTimestamps = field(default_factory=LocalTimestamps)
    facebook: dict | None = None
    google: dict | None = None
    apple: dict | None = None


@dataclass(kw_only=True)
class UltimateGearSetsAchievments(BaseModel):
    """Achievments ultimateGearSets data."""

    healer: bool | None = None
    wizard: bool | None = None
    rogue: bool | None = None
    warrior: bool | None = None


@dataclass(kw_only=True)
class QuestsAchievments(BaseModel):
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
class AchievementsUser(BaseModel):
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
class BackerUser(BaseModel):
    """User backer data."""

    tier: int | None = None
    npc: str | None = None
    tokensApplied: bool | None = None


@dataclass(kw_only=True)
class PermissionsUser(BaseModel):
    """User permissions data."""

    fullAccess: bool | None = None
    news: bool | None = None
    userSupport: bool | None = None
    challengeAdmin: bool | None = None
    moderator: bool | None = None
    coupons: bool | None = None


@dataclass(kw_only=True)
class ContributorUser(BaseModel):
    """User contributer data."""

    contributions: str | None = None
    level: int | None = None
    text: str | None = None


@dataclass(kw_only=True)
class ConsecutivePlan(BaseModel):
    """Plan consecutive data."""

    trinkets: int | None = None
    gemCapExtra: int | None = None
    offset: int | None = None
    count: int | None = None


@dataclass(kw_only=True)
class PlanPurchased(BaseModel):
    """Purchased background data."""

    consecutive: ConsecutivePlan = field(default_factory=ConsecutivePlan)
    mysteryItems: list = field(default_factory=list)
    gemsBought: int | None = None
    extraMonths: int | None = None
    dateUpdated: datetime | None = None
    perkMonthCount: int | None = None
    quantity: int | None = None


@dataclass(kw_only=True)
class PurchasedUser(BaseModel):
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
class TourFlags(BaseModel):
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
class CommonTutorial(BaseModel):
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
class IosTutorial(BaseModel):
    """Tutorial ios data."""

    addTask: bool
    editTask: bool
    deleteTask: bool
    filterTask: bool
    groupPets: bool
    inviteParty: bool
    reorderTask: bool


@dataclass(kw_only=True)
class TutorialFlags(BaseModel):
    """Flags tutorial data."""

    common: CommonTutorial | None = None
    ios: IosTutorial | None = None


@dataclass(kw_only=True)
class FlagsUser(BaseModel):
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
class EntryHistory(BaseModel):
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
class HistoryUser(BaseModel):
    """User history data."""

    todos: list[EntryHistory] = field(default_factory=list)
    exp: list[EntryHistory] = field(default_factory=list)


@dataclass(kw_only=True)
class GearItems(GearItemsAvatar, BaseModel):
    """Items gear data."""

    owned: dict[str, bool] = field(default_factory=dict)


@dataclass(kw_only=True)
class SpecialItems(BaseModel):
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
class LastDropItems(BaseModel):
    """LastDrop items data."""

    count: int | None = None
    date: datetime | None = None


@dataclass(kw_only=True)
class ItemsUser(ItemsAvatar, BaseModel):
    """User items data."""

    gear: GearItems = field(default_factory=GearItems)
    special: SpecialItems = field(default_factory=SpecialItems)
    lastDrop: LastDropItems = field(default_factory=LastDropItems)
    quests: dict[str, int] = field(default_factory=dict)
    mounts: dict[str, bool] = field(default_factory=dict)
    food: dict[str, int] = field(default_factory=dict)
    hatchingPotions: dict[str, int] = field(default_factory=dict)
    eggs: dict[str, int] = field(default_factory=dict)
    pets: dict[str, int] = field(default_factory=dict)


@dataclass(kw_only=True)
class InvitationsUser(BaseModel):
    """Invitations user data."""

    party: dict = field(default_factory=dict)
    guilds: list = field(default_factory=list)
    parties: list = field(default_factory=list)


@dataclass(kw_only=True)
class ProgressQuest(BaseModel):
    """Quest progress data."""

    up: float | None = None
    down: float | None = None
    collect: dict = field(default_factory=dict)
    collectedItems: int | None = None


@dataclass(kw_only=True)
class QuestParty(BaseModel):
    """Party quest data."""

    progress: ProgressQuest = field(default_factory=ProgressQuest)
    RSVPNeeded: bool | None = None
    key: str | None = None
    completed: str | None = None
    active: bool | None = None
    leader: UUID | None = None
    members: dict[UUID, bool] = field(default_factory=dict)


@dataclass(kw_only=True)
class PartyUser(BaseModel):
    """Party user data."""

    quest: QuestParty = field(default_factory=QuestParty)
    order: str | None = None
    orderAscending: str | None = None
    _id: UUID | None = None


@dataclass(kw_only=True)
class EmailNotificationsPreferences(BaseModel):
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
class PushNotificationsPreferences(BaseModel):
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
class SuppressModalsPreferences(BaseModel):
    """SupressModals preferences data."""

    levelUp: bool | None = None
    hatchPet: bool | None = None
    raisePet: bool | None = None
    streak: bool | None = None


@dataclass(kw_only=True)
class ActiveFilterTask(BaseModel):
    """ActiveFilter task data."""

    habit: str | None = None
    daily: str | None = None
    todo: str | None = None
    reward: str | None = None


@dataclass(kw_only=True)
class TasksPreferences(BaseModel):
    """Tasks preferences data."""

    activeFilter: ActiveFilterTask = field(default_factory=ActiveFilterTask)
    groupByChallenge: bool | None = None
    confirmScoreNotes: bool | None = None
    mirrorGroupTasks: list[UUID] = field(default_factory=list)


@dataclass(kw_only=True)
class PreferencesUser(PreferencesAvatar, BaseModel):
    """Preferences user data."""

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
    hideHeader: bool | None = None
    timezoneOffset: int | None = None
    sound: str | None = None
    allocationMode: str | None = None
    autoEquip: bool | None = None
    dateFormat: str | None = None
    stickyHeader: bool | None = None
    disableClasses: bool | None = None
    newTaskEdit: bool | None = None
    dailyDueDefaultView: bool | None = None
    advancedCollapsed: bool | None = None
    toolbarCollapsed: bool | None = None
    reverseChatOrder: bool | None = None
    developerMode: bool | None = None
    displayInviteToPartyWhenPartyIs1: bool | None = None
    automaticAllocation: bool | None = None
    webhooks: dict = field(default_factory=dict)
    improvementCategories: list[str] = field(default_factory=list)
    timezoneOffsetAtLastCron: int | None = None
    language: Language | None = None


@dataclass(kw_only=True)
class ProfileUser(BaseModel):
    """Profile user data."""

    blurb: str | None = None
    imageUrl: str | None = None
    name: str | None = None


@dataclass(kw_only=True)
class BuffsStats(BuffsStatsavatar, BaseModel):
    """Buffs stats data."""

    Str: int | None = None
    per: int | None = None
    con: int | None = None
    stealth: int | None = None
    streaks: bool | None = None
    seafoam: bool | None = None
    shinySeed: bool | None = None
    snowball: bool | None = None
    spookySparkles: bool | None = None
    Int: int | None = None


@dataclass(kw_only=True)
class TrainingStats(BaseModel):
    """Training stats data."""

    Str: float | None = None
    per: int | None = None
    con: int | None = None
    Int: int | None = None


@dataclass(kw_only=True)
class StatsUser(StatsAvatar, BaseModel):
    """Stats user data."""

    buffs: BuffsStats = field(default_factory=BuffsStats)
    training: TrainingStats = field(default_factory=TrainingStats)
    hp: float | None = None
    mp: float | None = None
    exp: int | None = None
    gp: float | None = None
    lvl: int | None = None
    points: int | None = None
    Str: int | None = None
    con: int | None = None
    per: int | None = None
    toNextLevel: int | None = None
    maxHealth: int | None = None
    maxMP: int | None = None
    Int: int | None = None


@dataclass(kw_only=True)
class TagsUser(BaseModel):
    """Tags user data."""

    id: UUID | None = None
    name: str | None = None
    challenge: bool | None = None
    group: str | None = None


@dataclass(kw_only=True)
class InboxUser(BaseModel):
    """Inbox user data."""

    newMessages: int | None = None
    optOut: bool | None = None
    blocks: list = field(default_factory=list)
    messages: dict = field(default_factory=dict)


@dataclass(kw_only=True)
class TasksOrderUser(BaseModel):
    """TasksOrder user data."""

    habits: list[UUID] = field(default_factory=list)
    dailys: list[UUID] = field(default_factory=list)
    todos: list[UUID] = field(default_factory=list)
    rewards: list[UUID] = field(default_factory=list)


@dataclass(kw_only=True)
class PushDevicesUser(BaseModel):
    """PushDevices user data."""

    regId: str
    Type: str
    createdAt: datetime
    updatedAt: datetime


class WebhookType(StrEnum):
    """Webhook types."""

    TASK_ACTIVITY = "taskActivity"
    USER_ACTIVITY = "userActivity"
    QUEST_ACTIVITY = "questActivity"
    GROUP_CHAT_RECEIVED = "groupChatReceived"
    GLOBAL_ACTIVITY = "globalActivity"


@dataclass(kw_only=True)
class QuestActivityOptions(BaseModel):
    """Quest activity options."""

    questStarted: bool = False
    questFinished: bool = False
    questInvited: bool = False


@dataclass(kw_only=True)
class UserActivityOptions(BaseModel):
    """User activity options."""

    petHatched: bool = False
    mountRaised: bool = False
    leveledUp: bool = False


@dataclass
class GroupChatReceivedOptions(BaseModel):
    """Group chat received options."""

    groupId: UUID


@dataclass(kw_only=True)
class TaskActivityOptions(BaseModel):
    """Task activity options."""

    created: bool = False
    updated: bool = False
    deleted: bool = False
    checklistScored: bool = False
    scored: bool = True


@dataclass(kw_only=True)
class Webhook(BaseModel):
    """Webhook base class."""

    url: str | None = field(default=None, kw_only=False)
    enabled: bool | None = None
    label: str | None = None
    id: UUID | None = None


@dataclass(kw_only=True)
class TaskActivity(Webhook):
    """Task activity."""

    Type: WebhookType = field(default=WebhookType.TASK_ACTIVITY, init=False)
    options: TaskActivityOptions = field(default_factory=TaskActivityOptions)


@dataclass(kw_only=True)
class GroupChatReceived(Webhook):
    """Group chat received."""

    def __post_init__(self) -> None:
        """Initialize the GroupChatReceived class."""
        if self.groupId:
            if not isinstance(self.groupId, UUID):
                self.groupId = UUID(self.groupId)

            self.options = GroupChatReceivedOptions(groupId=self.groupId)
            self.groupId = None

    groupId: UUID | str | None = field(default=None, kw_only=False)
    Type: WebhookType = field(default=WebhookType.GROUP_CHAT_RECEIVED, init=False)
    options: GroupChatReceivedOptions = field(init=False)


@dataclass(kw_only=True)
class UserActivity(Webhook):
    """User activity."""

    Type: WebhookType = field(default=WebhookType.USER_ACTIVITY, init=False)
    options: UserActivityOptions = field(default_factory=UserActivityOptions)


@dataclass(kw_only=True)
class QuestActivity(Webhook):
    """Quest activity."""

    Type: WebhookType = field(default=WebhookType.QUEST_ACTIVITY, init=False)
    options: QuestActivityOptions = field(default_factory=QuestActivityOptions)


@dataclass(kw_only=True)
class GlobalActivity(Webhook):
    """Global  activity.

    Note: global webhooks send a request for every type of event
    """

    Type: WebhookType = field(default=WebhookType.GLOBAL_ACTIVITY, init=False)


class HabiticaWebhookResponse(HabiticaResponse):
    """Representation of a webhook data response."""

    data: Annotated[
        Webhook,
        Discriminator(
            field="type",
            include_subtypes=True,
        ),
    ]


class HabiticaDeleteWebhookResponse(HabiticaResponse):
    """Representation of a delete webhook response."""

    data: list[
        Annotated[
            Webhook,
            Discriminator(
                field="type",
                include_subtypes=True,
            ),
        ]
    ]


@dataclass(kw_only=True)
class WebhookUser(BaseModel):
    """Webhooks user data."""

    failures: int = 0
    lastFailureAt: datetime | None = None
    createdAt: datetime | None = None
    updatedAt: datetime | None = None


@dataclass(kw_only=True)
class TaskActivityWebhook(WebhookUser, TaskActivity):
    """Task activity webhook."""

    type = "taskActivity"


@dataclass(kw_only=True)
class QuestActivityWebhook(WebhookUser, QuestActivity):
    """Quest activity webhook."""

    type = "questActivity"


@dataclass(kw_only=True)
class GlobalActivityWebhook(WebhookUser, GlobalActivity):
    """Global activity webhook."""

    type = "globalActivity"


@dataclass(kw_only=True)
class GroupChatReceivedWebhook(WebhookUser, GroupChatReceived):
    """Group chat received webhook."""

    type = "groupChatReceived"
    groupId: None = None
    options: GroupChatReceivedOptions = field(init=True)


@dataclass(kw_only=True)
class UserActivityWebhook(WebhookUser, UserActivity):
    """User activity webhook."""

    type = "userActivity"


@dataclass(kw_only=True)
class PinnedItemsUser(BaseModel):
    """PinnedItems user data."""

    path: str
    Type: str


@dataclass(kw_only=True)
class UserData(Avatar, BaseModel):
    """User data."""

    id: UUID | None = None
    preferences: PreferencesUser = field(default_factory=PreferencesUser)
    flags: FlagsUser = field(default_factory=FlagsUser)
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
    webhooks: list[
        Annotated[
            Webhook,
            Discriminator(
                field="type",
                include_subtypes=True,
            ),
        ]
    ] = field(default_factory=list)
    loginIncentives: int | None = None
    invitesSent: int | None = None
    pinnedItems: list[PinnedItemsUser] = field(default_factory=list)
    pinnedItemsOrder: list[str] = field(default_factory=list)
    unpinnedItems: list[PinnedItemsUser] = field(default_factory=list)
    secret: str | None = None
    balance: float | None = None
    lastCron: datetime | None = None
    needsCron: bool | None = None
    challenges: list[UUID] = field(default_factory=list)
    guilds: list[UUID] = field(default_factory=list)
    newMessages: dict[str, bool] = field(default_factory=dict)


class HabiticaUserResponse(HabiticaResponse):
    """Representation of a user data response."""

    data: UserData


@dataclass(kw_only=True)
class HabiticaGroupMembersResponse(HabiticaResponse):
    """Representation of a group members data response."""

    data: list[UserData]


@dataclass(kw_only=True)
class CompletedBy(BaseModel):
    """Task group completedby data."""

    userId: UUID | None = None
    date: datetime | None = None


@dataclass(kw_only=True)
class GroupTask(BaseModel):
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
class Repeat(BaseModel):
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
class Challenge(BaseModel):
    """Challenge task data."""

    id: UUID | None = None
    taskId: UUID | None = None
    shortName: str | None = None
    broken: ChallengeAbortedReason | None = None
    winner: str | None = None


@dataclass(kw_only=True)
class Reminders(BaseModel):
    """Task reminders data."""

    id: UUID
    time: datetime
    startDate: datetime | None = None


@dataclass(kw_only=True)
class Checklist(BaseModel):
    """Task checklist data."""

    id: UUID
    text: str
    completed: bool


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


class Task(TypedDict("Task", {"type": NotRequired[TaskType]}), total=True):
    """Representation of a task."""

    text: NotRequired[str]
    attribute: NotRequired[Attributes]
    alias: NotRequired[str]
    notes: NotRequired[str]
    tags: NotRequired[list[UUID]]
    collapseChecklist: NotRequired[bool]
    date: NotRequired[datetime | dt.date | None]
    priority: NotRequired[TaskPriority]
    reminders: NotRequired[list[Reminders]]
    checklist: NotRequired[list[Checklist]]
    up: NotRequired[bool]
    down: NotRequired[bool]
    counterUp: NotRequired[int]
    counterDown: NotRequired[int]
    startDate: NotRequired[datetime | dt.date]
    frequency: NotRequired[Frequency]
    everyX: NotRequired[int]
    repeat: NotRequired[Repeat]
    daysOfMonth: NotRequired[list[int]]
    weeksOfMonth: NotRequired[list[int]]
    completed: NotRequired[bool]
    streak: NotRequired[int]
    value: NotRequired[float]


@dataclass(kw_only=True)
class TaskData(BaseModel):
    """Task data."""

    challenge: Challenge = field(default_factory=Challenge)
    group: GroupTask = field(default_factory=GroupTask)
    Type: TaskType | None = None
    text: str | None = None
    notes: str | None = None
    tags: list[UUID] = field(default_factory=list)
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
    history: list[EntryHistory] = field(default_factory=list)
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
    checklist: list[Checklist] = field(default_factory=list)
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
class HabiticaErrorResponse(BaseModel):
    """Base class for Habitica errors."""

    success: bool
    error: str
    message: str


@dataclass(kw_only=True)
class TasksUserExport(BaseModel):
    """Tasks user export data."""

    todos: list[TaskData] = field(default_factory=list)
    dailys: list[TaskData] = field(default_factory=list)
    habits: list[TaskData] = field(default_factory=list)
    rewards: list[TaskData] = field(default_factory=list)


@dataclass(kw_only=True)
class HabiticaUserExport(UserData, BaseModel):
    """Representation of a user data export."""

    tasks: TasksUserExport = field(default_factory=TasksUserExport)


@dataclass
class UserAnonymizedData:
    """Anonymized user data."""

    user: UserData = field(default_factory=UserData)
    tasks: list[TaskData] = field(default_factory=list)


@dataclass(kw_only=True)
class HabiticaUserAnonymizedResponse(BaseModel):
    """Representation of a anonymized user data export."""

    data: UserAnonymizedData


@dataclass(kw_only=True)
class HabiticaStatsResponse(HabiticaResponse):
    """Representation of a response containing stats data."""

    data: StatsUser


@dataclass(kw_only=True)
class QuestTmpScore(BaseModel):
    """Represents the quest progress details."""

    progressDelta: float | None = None
    collection: int | None = None


@dataclass(kw_only=True)
class DropTmpScore(BaseModel):
    """Represents the details of an item drop."""

    target: str | None = None
    canDrop: bool | None = None
    value: int | None = None
    key: str | None = None
    Type: str | None = None
    dialog: str | None = None


@dataclass(kw_only=True)
class TmpScore(BaseModel):
    """Temporary quest and drop data."""

    quest: QuestTmpScore = field(default_factory=QuestTmpScore)
    drop: DropTmpScore = field(default_factory=DropTmpScore)


@dataclass
class ScoreData(StatsUser):
    """Scora data."""

    delta: float | None = None
    tmp: TmpScore = field(default_factory=TmpScore)


@dataclass(kw_only=True)
class HabiticaScoreResponse(HabiticaResponse):
    """Representation of a score response."""

    data: ScoreData


@dataclass(kw_only=True)
class HabiticaTagsResponse(HabiticaResponse):
    """Representation of a score response."""

    data: list[TagsUser]


@dataclass(kw_only=True)
class HabiticaTagResponse(HabiticaResponse):
    """Representation of a score response."""

    data: TagsUser


@dataclass(kw_only=True)
class QuestData(BaseModel):
    """Quest data."""

    progress: ProgressQuest = field(default_factory=ProgressQuest)
    active: bool = False
    members: dict[str, bool | None]
    extra: dict | None = None
    key: str
    leader: UUID | None = None


@dataclass(kw_only=True)
class HabiticaQuestResponse(HabiticaResponse):
    """Representation of a quest response."""

    data: QuestData


@dataclass
class ChangeClassData(BaseModel):
    """Change class data."""

    preferences: PreferencesUser = field(default_factory=PreferencesUser)
    flags: FlagsUser = field(default_factory=FlagsUser)
    items: ItemsUser = field(default_factory=ItemsUser)
    stats: StatsUser = field(default_factory=StatsUser)


@dataclass(kw_only=True)
class HabiticaClassSystemResponse(HabiticaResponse):
    """Representation of a change-class response."""

    data: ChangeClassData


@dataclass
class HabiticaTaskOrderResponse(HabiticaResponse):
    """Representation of a reorder task response."""

    data: list[UUID] = field(default_factory=list)


@dataclass
class HabiticaSleepResponse(HabiticaResponse):
    """Representation of a sleep response."""

    data: bool


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
    PICKPOCKET = "pickPocket"
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


@dataclass
class AchievmentContent(BaseModel):
    """Achievment content data."""

    icon: str
    key: str
    titleKey: str | None = None
    textKey: str | None = None
    singularTitleKey: str | None = None
    singularTextKey: str | None = None
    pluralTitleKey: str | None = None
    pluralTextKey: str | None = None


@dataclass
class AnimalColorAchievementContent(BaseModel):
    """animalColorAchievement content data."""

    color: str
    petAchievement: str
    petNotificationType: str
    mountAchievement: str
    mountNotificationType: str


@dataclass
class AnimalSetAchievementContent(BaseModel):
    """animalSetAchievements content data."""

    Type: str
    species: list[str]
    achievementKey: str
    notificationType: str


@dataclass
class StableAchievementContent(BaseModel):
    """stableAchievements content data."""

    masterAchievement: str
    masterNotificationType: str


@dataclass
class PetSetCompleteAchievsContent(BaseModel):
    """petSetCompleteAchievs content data."""

    color: str
    petAchievement: str
    petNotificationType: str


@dataclass
class QuestBossRage(BaseModel):
    """QuestBossRage content data."""

    title: str
    description: str
    value: float
    effect: str | None = None
    healing: float | None = None


@dataclass
class QuestBoss(BaseModel):
    """QuestBoss content data."""

    name: str
    hp: float
    Str: float
    Def: float
    rage: QuestBossRage | None = None


@dataclass
class QuestItem(BaseModel):
    """QuestItem content data."""

    Type: str
    key: str
    text: str


@dataclass
class QuestDrop(BaseModel):
    """QuestDrop content data."""

    gp: float
    exp: float
    items: list[QuestItem] = field(default_factory=list)


@dataclass
class QuestCollect(BaseModel):
    """QuestCollect content data."""

    text: str
    count: int


@dataclass
class QuestUnlockCondition(BaseModel):
    """QuestUnlockCondition content data."""

    condition: str
    text: str


@dataclass
class QuestsContent(BaseModel):
    """petSetCompleteAchievs content data."""

    text: str
    notes: str

    completion: str
    category: str

    drop: QuestDrop
    key: str
    goldValue: float | None = None
    value: float | None = None
    previous: str | None = None
    prereqQuests: list[str] | None = None
    collect: dict[str, QuestCollect] | None = None
    unlockCondition: QuestUnlockCondition | None = None
    boss: QuestBoss | None = None
    group: str | None = None


@dataclass
class ItemListEntry(BaseModel):
    """ItemListEntry content data."""

    localeKey: str
    isEquipment: bool


@dataclass
class ItemListContent(BaseModel):
    """ItemListContent content data."""

    weapon: ItemListEntry
    armor: ItemListEntry
    head: ItemListEntry
    shield: ItemListEntry
    back: ItemListEntry
    body: ItemListEntry
    headAccessory: ItemListEntry
    eyewear: ItemListEntry
    hatchingPotions: ItemListEntry
    premiumHatchingPotions: ItemListEntry
    eggs: ItemListEntry
    quests: ItemListEntry
    food: ItemListEntry
    Saddle: ItemListEntry
    bundles: ItemListEntry


@dataclass(kw_only=True)
class GearEntry(BaseModel):
    """GearEntry content data."""

    text: str
    notes: str
    Int: int
    value: int
    Type: str
    key: str
    Set: str
    klass: str
    index: str
    Str: int
    per: int
    con: int


@dataclass
class GearClass(BaseModel):
    """GearClass content data."""

    base: dict[str, GearEntry] | None = None
    warrior: dict[str, GearEntry] | None = None
    wizard: dict[str, GearEntry] | None = None
    rogue: dict[str, GearEntry] | None = None
    special: dict[str, GearEntry] | None = None
    armoire: dict[str, GearEntry] | None = None
    mystery: dict[str, GearEntry] | None = None
    healer: dict[str, GearEntry] | None = None


@dataclass
class GearType(BaseModel):
    """GearType content data."""

    weapon: GearClass
    armor: GearClass
    head: GearClass
    shield: GearClass
    back: GearClass
    body: GearClass
    headAccessory: GearClass
    eyewear: GearClass


@dataclass
class GearContent(BaseModel):
    """GearContent content data."""

    tree: GearType
    flat: dict[str, GearEntry]


@dataclass
class SpellEntry(BaseModel):
    """SpellEntry content data."""

    text: str
    mana: int
    target: str
    notes: str
    key: str
    previousPurchase: bool | None = None
    limited: bool | None = None
    lvl: int | None = None
    value: int | None = None
    immediateUse: bool | None = None
    purchaseType: str | None = None
    silent: bool | None = None


@dataclass
class SpellsClass(BaseModel):
    """SpellsClass content data."""

    wizard: dict[str, SpellEntry]
    warrior: dict[str, SpellEntry]
    rogue: dict[str, SpellEntry]
    healer: dict[str, SpellEntry]
    special: dict[str, SpellEntry]


@dataclass
class CardTypes(BaseModel):
    """CardTypes content data."""

    key: str
    messageOptions: int
    yearRound: bool = False


@dataclass
class SpecialItemEntry(BaseModel):
    """Item content data."""

    key: str | None = None
    text: str | None = None
    notes: str | None = None
    immediateUse: bool | None = None
    limited: bool | None = None
    mana: int | None = None
    previousPurchase: bool | None = None
    purchaseType: str | None = None
    silent: bool | None = None
    target: str | None = None
    value: int | None = None


@dataclass
class EggEntry(BaseModel):
    """Egg content data."""

    text: str | None = None
    mountText: str | None = None
    adjective: str | None = None
    value: int | None = None
    key: str | None = None
    notes: str | None = None


@dataclass
class HatchingPotionEntry(BaseModel):
    """Hatching potion content data."""

    value: int | None = None
    key: str | None = None
    text: str | None = None
    notes: str | None = None
    premium: bool | None = None
    limited: bool | None = None
    _addlNotes: str | None = None
    wacky: bool | None = None


@dataclass
class PetEntry(BaseModel):
    """Pet content data."""

    key: str | None = None
    Type: str | None = None
    potion: str | None = None
    egg: str | None = None
    text: str | None = None


@dataclass(kw_only=True)
class InventoryItemEntry(BaseModel):
    """Inventory item content data."""

    text: str | None = None
    textA: str | None = None
    textThe: str | None = None
    target: str | None = None
    value: int | None = None
    key: str | None = None
    notes: str | None = None
    canDrop: bool | None = None
    sellWarningNote: str | None = None


@dataclass(kw_only=True)
class Achievment(BaseModel):
    """An achievment."""

    icon: str
    titleKey: str
    textKey: str
    key: str
    text2Key: str | None = None
    notificationText: str | None = None
    singularTitleKey: str | None = None
    singularTextKey: str | None = None
    pluralTitleKey: str | None = None
    pluralTextKey: str | None = None
    modalTextKey: str | None = None


@dataclass(kw_only=True)
class Incentive(BaseModel):
    """A login incentive."""

    rewardKey: list[str] = field(default_factory=list)
    nextRewardAt: int = 500
    prevRewardKey: int = 0
    reward: list[QuestsContent | GearEntry | InventoryItemEntry | Achievment] = field(
        default_factory=list
    )


@dataclass
class ContentData(BaseModel):
    """Content data."""

    achievements: dict[str, AchievmentContent]
    questSeriesAchievements: dict[str, list[str]]
    animalColorAchievements: list[AnimalColorAchievementContent]
    animalSetAchievements: dict[str, AnimalSetAchievementContent]
    stableAchievements: dict[str, StableAchievementContent]
    petSetCompleteAchievs: list[PetSetCompleteAchievsContent]
    quests: dict[str, QuestsContent]
    questsByLevel: list[QuestsContent]
    userCanOwnQuestCategories: list[str]
    itemList: ItemListContent
    gear: GearContent
    spells: SpellsClass
    audioThemes: list[str]
    # mystery
    officialPinnedItems: list
    # bundles
    # potion
    # armoire
    # events
    # repeatingEvents
    classes: list[str]
    gearTypes: list[str]
    cardTypes: dict[str, CardTypes]
    special: dict[str, SpecialItemEntry]
    dropEggs: dict[str, EggEntry]
    questEggs: dict[str, EggEntry]
    eggs: dict[str, EggEntry]
    # timeTravelStable
    dropHatchingPotions: dict[str, HatchingPotionEntry]
    premiumHatchingPotions: dict[str, HatchingPotionEntry]
    wackyHatchingPotions: dict[str, HatchingPotionEntry]
    hatchingPotions: dict[str, HatchingPotionEntry]
    pets: dict[str, bool]
    premiumPets: dict[str, bool]
    questPets: dict[str, bool]
    specialPets: dict[str, str]
    wackyPets: dict[str, bool]
    petInfo: dict[str, PetEntry]
    mounts: dict[str, bool]
    premiumMounts: dict[str, bool]
    questMounts: dict[str, bool]
    specialMounts: dict[str, str]
    mountInfo: dict[str, PetEntry]
    food: dict[str, InventoryItemEntry]
    # appearances
    # backgrounds
    # backgroundsFlat
    # userDefaults
    # tasksByCategory
    # userDefaultsMobile
    # faq
    loginIncentives: dict[str, Incentive]


@dataclass
class HabiticaContentResponse(HabiticaResponse):
    """Representation of a content response."""

    data: ContentData


@dataclass
class PartyMember(BaseModel):
    """Party member data."""

    stats: StatsUser
    achievements: AchievementsUser
    items: ItemsUser
    profile: ProfileUser


@dataclass
class UserTasks(BaseModel):
    """User and tasks data."""

    user: UserData
    partyMembers: list[PartyMember] = field(default_factory=list)
    task: TaskData | None = None


@dataclass
class HabiticaCastSkillResponse(HabiticaResponse):
    """Representation of a cast skill response."""

    data: UserTasks


class GroupPrivacy(StrEnum):
    """Group privacy."""

    PRIVATE = "private"
    PUBLIC = "public"


class GroupType(StrEnum):
    """Group type."""

    GUILD = "guild"
    PARTY = "party"


@dataclass(kw_only=True)
class LeaderOnly(BaseModel):
    """Group leaderOnly  data."""

    challenges: bool
    getGems: bool


@dataclass(kw_only=True)
class GroupLeader(BaseModel):
    """Group leader data."""

    id: UUID
    auth: AuthUser
    profile: ProfileUser


@dataclass(kw_only=True)
class ChatMsgInfo(BaseModel):
    """Chat message info."""

    type: str | None = None
    user: str | None = None
    quest: str | None = None
    items: dict[str, int] | None = None


@dataclass(kw_only=True)
class ChatMsg(BaseModel):
    """Chat message."""

    id: UUID
    flagCount: int
    text: str
    unformattedText: str
    info: ChatMsgInfo
    timestamp: datetime = field(
        metadata=field_options(
            deserialize=serialize_datetime,
        )
    )
    likes: dict[UUID, bool]
    client: str | None = None
    uuid: UUID | str
    groupId: UUID | None = None
    user: str | None = None
    username: str | None = None
    userStyles: Avatar | None = None
    sent: bool | None = None
    ownerId: UUID | None = None
    uniqueMessageId: UUID | None = None


@dataclass(kw_only=True)
class GroupData(BaseModel):
    """Groups data."""

    name: str
    summary: str = ""
    description: str = ""
    leader: GroupLeader
    type: GroupType
    privacy: GroupPrivacy
    chat: list[ChatMsg]
    leaderOnly: LeaderOnly
    memberCount: int = 1
    ChallengeCount: int = 0
    chatLimitCount: int | None = None
    balance: float
    logo: str | None = None
    leaderMessage: str | None = None
    quest: QuestParty


@dataclass
class HabiticaGroupsResponse(HabiticaResponse):
    """Representation of a groups response."""

    data: GroupData


@dataclass(kw_only=True)
class MessageData(BaseModel):
    """Message data."""

    message: ChatMsg


@dataclass(kw_only=True)
class HabiticaMessageResponse(HabiticaResponse):
    """Representation of a group response."""

    data: MessageData
