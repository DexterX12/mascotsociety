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
    ERROR: int = 600
    ITEM_DOES_NOT_EXIST: int = 601
    COMPONENT_DOES_NOT_EXIST: int = 602
    COMPONENT_PURCHASED: int = 603
    ITEM_PURCHASED: int = 604
    COMPONENT_ALREADY_COMPLETED: int = 605
    ITEM_ALREADY_COMPLETED: int = 606
    NOT_ENOUGH_CREDITS: int = 607
    ITEM_INFO_FOUND: int = 608
    ITEM_CLAIMED: int = 609
    UNABLE_TO_CLAIM_ITEM: int = 610
    ERROR_ADDING_CLAIMED_ITEM: int = 611

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
    MINI_GAME_DATA_DOES_NOT_EXIST: int = 6000
    MINI_GAME_DATA_PURCHASED: int = 6001
    MINI_GAME_DATA_INFO_FOUND: int = 6002
    MINI_GAME_ERROR_ADDING_DATA: int = 6003
    MINI_GAME_DATA_ERROR: int = 6004
    MINI_GAME_DATA_NOT_ENOUGH_CREDITS: int = 6005
    MINI_GAME_DATA_SAVED: int = 6006
    MINI_GAME_DATA_NOT_ENOUGH_GAME_SPECIFIC_CASH: int = 5906

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
    DIY_ITEM_DOES_NOT_EXIST: int = 5900
    DIY_COMPONENT_DOES_NOT_EXIST: int = 5901
    DIY_COMPONENT_PURCHASED: int = 5902
    DIY_ITEM_PURCHASED: int = 5903
    DIY_COMPONENT_ALREADY_COMPLETED: int = 5904
    DIY_ITEM_ALREADY_COMPLETED: int = 5905
    DIY_NOT_ENOUGH_CREDITS: int = 5906
    DIY_ITEM_INFO_FOUND: int = 5907
    DIY_ITEM_CLAIMED: int = 5908
    DIY_UNABLE_TO_CLAIM_ITEM: int = 5909
    DIY_ERROR_ADDING_CLAIMED_ITEM: int = 5910
    DIY_ERROR: int = 5911

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
    PETS_QUEST_DATA_DOES_NOT_EXIST: int = 6010
    PETS_QUEST_DATA_PURCHASED: int = 6011
    PETS_QUEST_DATA_INFO_FOUND: int = 6012
    PETS_QUEST_ERROR_ADDING_DATA: int = 6013
    PETS_QUEST_DATA_ERROR: int = 6014
    PETS_QUEST_DATA_NOT_ENOUGH_CREDITS: int = 6015
    PETS_QUEST_ACTIVITY_SAVED: int = 6016
    PETS_QUEST_STAGE_SAVED: int = 6017
    PETS_SUBQUEST_DATA_DOES_NOT_EXIST: int = 6018
    PETS_QUEST_UNABLE_TO_CLAIM_ITEM: int = 6019
    PETS_QUEST_ITEM_CLAIMED: int = 6020
    PETS_QUSET_ERROR_ADDING_CLAIMED_ITEM: int = 6021
    PETS_QUEST_ACTIVITY_PURCHASED: int = 6024
    PETS_QUEST_GRACE_HOURS_ADDED: int = 6025

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

