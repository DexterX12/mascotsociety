from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from ..datatypes import MultiTypeMap
from ..share import NetworkUid

@dataclass
class AuditChange:
    action: int = 0
    newCredits: int = 0
    newRecyclePoints: int = 0
    newStickerPoints: int = 0
    creditsDelta: int = 0
    token: str = ""
    newItemId: int = 0
    itemId: int = 0
    itemHash: int = 0
    active: bool = False
    roomIndex: int = 0
    positionX: int = 0
    positionY: int = 0
    positionZ: int = 0
    createTime: Optional[datetime] = None
    containedItem: int = 0
    containedType: int = 0
    containedAmount: int = 0
    sender: Optional[NetworkUid] = None
    accompanyingItemId: int = 0
    message: str = ""
    csum: int = 0

    def __str__(self) -> str:
        return (
            f"[AuditChange: action={self.action} newCredits={self.newCredits} "
            f"creditsDelta={self.creditsDelta} newRecyclePoints={self.newRecyclePoints} "
            f"newStickerPoints={self.newStickerPoints} token={self.token} "
            f"newItemId={self.newItemId} itemId={self.itemId} itemHash={self.itemHash} "
            f"active={self.active} roomIndex={self.roomIndex} positionX={self.positionX} "
            f"positionY={self.positionY} positionZ={self.positionZ} createTime={self.createTime} "
            f"containedItem={self.containedItem} containedType={self.containedType} "
            f"containedAmount={self.containedAmount} sender={self.sender} message=\"{self.message}\"]"
        )


@dataclass
class AuditChangeBatch:
    saveVersion: int = 0
    auditChanges: List[AuditChange] = field(default_factory=list)
    visitedUids: List[NetworkUid] = field(default_factory=list)


@dataclass
class RpcOwnedItem:
    itemId: int = 0
    itemHash: int = 0
    active: bool = False
    roomIndex: int = 0
    positionX: int = 0
    positionY: int = 0
    positionZ: int = 0
    createTime: Optional[datetime] = None
    containedItem: int = 0
    containedItem2: int = 0
    containedType: int = 0
    containedAmount: int = 0
    sender: Optional[NetworkUid] = None
    message: str = ""
    itemProperties: Optional[MultiTypeMap] = None
    containedItemProperties: Optional[MultiTypeMap] = None
    containedItem2Properties: Optional[MultiTypeMap] = None

    def __str__(self) -> str:
        return (
            "[OwnedItem: itemId={self.itemId} itemHash={self.itemHash} "
            "active={self.active} roomIndex={self.roomIndex} positionX={self.positionX} "
            "positionY={self.positionY} positionZ={self.positionZ} createTime={self.createTime} "
            "containedItem={self.containedItem} containedItem2={self.containedItem2} "
            "containedType={self.containedType} containedAmount={self.containedAmount} "
            "sender={self.sender} message=\"{self.message} itemProperties={self.itemProperties}\"]"
        ).format(self=self)

@dataclass
class FeedLinkRecipient:
    recipient: Optional[NetworkUid] = None
    clickedDate: Optional[datetime] = None

    def __str__(self) -> str:
        return f"[FeedLinkRecipient: recipient={self.recipient} clickedDate={self.clickedDate}\"]"

@dataclass
class FeedLink:
    creationDate: Optional[datetime] = None
    itemHash: int = 0
    recipients: List[FeedLinkRecipient] = field(default_factory=list)
    rewardClaimed: bool = False

    def __str__(self) -> str:
        return (
            f"[FeedLink: itemHash={self.itemHash} creationDate={self.creationDate} "
            f"recipients={self.recipients} rewardClaimed={self.rewardClaimed}\"]"
        )

@dataclass
class DailyBonusInfo:
    isDailyBonusEnabled: bool = False
    canClaimDailyBonus: bool = False
    dailyBonusDay: int = 0

@dataclass
class LimitedItem:
    itemHash: int = 0
    amountSold: int = 0
    amountForSale: int = 0
    soldDate: Optional[datetime] = None
    dailyPurchaseLimit: int = 0
    isCashItem: bool = False

    def __str__(self) -> str:
        return (
            "LimitedItem: itemHash: {self.itemHash}, amountSold: {self.amountSold}, "
            "amountForSale: {self.amountForSale}, soldDate: {self.soldDate}, "
            "isCashItem: {self.isCashItem}, dailyPurchaseLimit: {self.dailyPurchaseLimit}"
        ).format(self=self)


class RpcCollaborativeBuildItem:

    def __init__(self) -> None:
        self.itemID: int = 0
        self._componentCount: Dict[str, int] = {}

    def setCount(self, component_id: int, count: int) -> None:
        self._componentCount[str(component_id)] = int(count)

    def getCount(self, component_id: int) -> int:
        return self._componentCount.get(str(component_id), 0)

    def __str__(self) -> str:
        parts = [f"CollaborativeItem: itemID: {self.itemID}"]
        for key, value in self._componentCount.items():
            parts.append(f"comp: {key}, count: {value}")
        return "\n".join(parts)


class RpcMiniGame:
    def __init__(self) -> None:
        self.gameID: int = 0
        self.triesLeft: int = 0
        self._elementData: Dict[str, float] = {}

    def setElementValue(self, element_id: int, value: float) -> None:
        self._elementData[str(element_id)] = float(value)

    def getElementValue(self, element_id: int) -> float:
        return self._elementData.get(str(element_id), 0.0)

    def __str__(self) -> str:
        parts = [f"MiniGame: itemID: {self.gameID}"]
        for key, value in self._elementData.items():
            parts.append(f"element: {key}, value: {value}")
        return "\n".join(parts)


class RpcDIYBuildItem:
    def __init__(self) -> None:
        self.itemID: int = 0
        self._componentCount: Dict[str, float] = {}

    def setTimeStamp(self, component_id: int, value: float) -> None:
        self._componentCount[str(component_id)] = float(value)

    def getTimeStamp(self, component_id: int) -> float:
        return self._componentCount.get(str(component_id), 0.0)

    def __str__(self) -> str:
        parts = [f"CollaborativeItem: itemID: {self.itemID}"]
        for key, value in self._componentCount.items():
            parts.append(f"comp: {key}, count: {value}")
        return "\n".join(parts)


class RpcWeeklyQuest:
    def __init__(self) -> None:
        self.questID: int = 0
        self.reward: int = 0
        self.graceHours: int = 0
        self._subQuestData: Dict[str, int] = {}
        self._subQuestRewards: Dict[str, str] = {}

    def setSubQuestInfo(self, subquest_id: int, value: int) -> None:
        self._subQuestData[str(subquest_id)] = int(value)

    def setSubQuestReward(self, subquest_id: int, reward: str) -> None:
        self._subQuestRewards[str(subquest_id)] = reward

    def getSubQuestInfo(self, subquest_id: int) -> int:
        return self._subQuestData.get(str(subquest_id), 0)

    def getSubQuestReward(self, subquest_id: int) -> str:
        return self._subQuestRewards.get(str(subquest_id), "")

    def __str__(self) -> str:
        parts = [
            f"WeeklyQuest: ID: {self.questID}",
            f", reward : {self.reward}",
            f", graceHours : {self.graceHours}",
        ]
        for key in self._subQuestData:
            parts.append(
                f"subQuestID: {key}, value: {self._subQuestData[key]}, reward = {self._subQuestRewards.get(key)}"
            )
        return " ".join(parts)
    
@dataclass
class RpcQuestReward:
    coins: int = 0
    itemId: int = 0
    itemHash: int = 0
    containedType: int = 0
    containedItem: int = 0
    xp: int = 0


@dataclass
class RpcQuestTracker:
    questId: int = 0
    stepsCompleted: int = 0


@dataclass
class RpcRewardTracker:
    rewardId: int = 0
    timesAwardedToday: int = 0


@dataclass
class RpcCounterEvent:
    userID: Optional[NetworkUid] = None
    counterEventID: int = 0
    aggregateID: int = 0
    eventType: int = 0
    triggerDate: Optional[datetime] = None
    eventStatus: int = 0
    senderID: Optional[NetworkUid] = None
    eventData: str = ""

