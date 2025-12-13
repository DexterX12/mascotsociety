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

class RpcCollaborativeBuildItem:

    def __init__(self) -> None:
        self.itemID: int = 0
        self._componentCount: Dict[str, int] = {}

    def setCount(self, component_id: int, count: int) -> None:
        self._componentCount[str(component_id)] = int(count)

    def getCount(self, component_id: int) -> int:
        return self._componentCount.get(str(component_id), 0)

    def iterComponentCounts(self):
        for key, value in self._componentCount.items():
            yield int(key), int(value)

    def __str__(self) -> str:
        parts = [f"CollaborativeItem: itemID: {self.itemID}"]
        for key, value in self._componentCount.items():
            parts.append(f"comp: {key}, count: {value}")
        return "\n".join(parts)
    
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

