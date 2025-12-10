from typing import Any, Dict, List, Optional

from ..datastream.input_data_stream import InputDataStream
from ..datatypes import MultiTypeMap, MultiTypeMapDatatype
from ..games.pets.builderquest import BuilderCollectable
from ..share import BitSet, NetworkUid
from .types import (
    AuditChange,
    AuditChangeBatch,
    FeedLink,
    FeedLinkRecipient,
    LimitedItem,
    RpcCollaborativeBuildItem,
    RpcDIYBuildItem,
    RpcMiniGame,
    RpcOwnedItem,
    RpcQuestTracker,
    RpcRewardTracker,
    RpcWeeklyQuest,
)
from .user_info import UserInfo


class RpcResponse:
    """Helper methods to read bytes regarding user data"""

    def __init__(self, stream: InputDataStream) -> None:
        self._stream = stream


    def __getattr__(self, name: str) -> Any:
        return getattr(self._stream, name)


    def readUserInfo(self) -> UserInfo:
        info = UserInfo()
        info.id = self.readNetworkUid()
        profile_fields = self._stream.readUintvar31()
        info.profileFields = profile_fields

        try:
            if UserInfo.containsAnyProfileField(profile_fields, UserInfo.FACEBOOK_INFO):
                info.usernameShort = self._stream.readString()
                info.usernameFull = self._stream.readString()
                info.imageUrl = self._stream.readString()
                info.profileUrl = self._stream.readString()

            if UserInfo.containsAnyProfileField(profile_fields, UserInfo.SCORE_AND_STATS):
                info.unavailable = self._read_relaxed_boolean(default=False)
                info.petName = self._stream.readString()
                info.credits = self._stream.readUintvar31()
                info.petPoints = self._stream.readUintvar31()
                info.petLevel = self._stream.readUint8()
                info.health = self._stream.readUint8()
                info.happiness = self._stream.readUint8()
                info.hygiene = self._stream.readUint8()
                info.primaryColour = self._stream.readUintvar31()
                info.preferencesMask = self._stream.readUint8()
                info.achievementsMask = self.readBitSet()
                info.lastSaveTime = self._stream.readDate()
                info.lastVisitTime = self._stream.readDate()
                info.streetPosition = self._stream.readUintvar31()
                info.recyclePoints = self._stream.readUintvar31()
                info.totalRecyclePoints = self._stream.readUintvar31()
                info.stickerPoints = self._stream.readUintvar31()
                info.totalStickerPoints = self._stream.readUintvar31()
                info.status = self._stream.readString()
                info.extraRooms = self._stream.readUint8()
                info.defaultRoomIndex = self._stream.readUint8()
                info.highScoreBall = self._stream.readUintvar31()
                info.highScoreFrisbee = self._stream.readUintvar31()
                info.highScoreJumpRope = self._stream.readUintvar31()
                info.numHatsBought = self._stream.readUintvar31()
                info.numShirtsBought = self._stream.readUintvar31()
                info.numTrousersBought = self._stream.readUintvar31()
                info.numShoesBought = self._stream.readUintvar31()
                info.numArmAccessoriesBought = self._stream.readUintvar31()
                info.numGiftsSent = self._stream.readUintvar31()
                info.numCoinsSpent = self._stream.readUintvar31()
                info.numVisit = self._stream.readUintvar31()
                info.numArenaHurdlesRaceWins = self._stream.readUintvar31()
                info.numArenaHurdlesBetWins = self._stream.readUintvar31()
                info.numProHurdlesRaceWins = self._stream.readUintvar31()
                info.numPlantsGrown = self._stream.readUintvar31()
                info.coinsWon = self._stream.readUintvar31()
                info.cookingPoints = self._stream.readUintvar31()
                info.recipesMask = self.readBitSet()
                info.petBirthday = self._stream.readDate()
                info.playCount = self._stream.readUintvar31()
                info.coinShovels = self._stream.readUintvar31()
                info.cashShovels = self._stream.readUintvar31()
                info.plotTopLeftX = self._stream.readIntvar32()
                info.plotTopLeftY = self._stream.readIntvar32()
                info.plotBottomRightX = self._stream.readIntvar32()
                info.plotBottomRightY = self._stream.readIntvar32()

            if UserInfo.containsAnyProfileField(
                profile_fields, UserInfo.OWNED_ITEMS, UserInfo.OWNED_EXTERIOR_ITEMS
            ):
                info.ownedItems = self._stream.readArray(self.readOwnedItem)

            if UserInfo.containsAnyProfileField(profile_fields, UserInfo.INACTIVE_ITEMS):
                info.completedSets = self._stream.readArray(self._stream.readUintvar32)
                info.tutorialMask = self.readBitSet()
                info.newsletterIndex = self._stream.readUintvar31()
                info.numArenaHurdlesRacesLeftToday = self._stream.readUintvar31()
                info.numProHurdlesRacesLeftToday = self._stream.readUintvar31()
                info.dailyArenaHurdlesBetProfit = self._stream.readUintvar31()
                info.checkoutVersion = self._stream.readUintvar31()
                info.lastPurchaseTime = self._stream.readDate()
                info.lastBookmarkPopupTime = self._stream.readDate()
                info.consecutiveLoginDays = self._stream.readUintvar31()
                info.lastLotteryTime = self._stream.readDate()

            if UserInfo.containsAnyProfileField(profile_fields, UserInfo.TRACKING_INFO):
                info.questTrackers = self._stream.readArray(self.readQuestTracker)

            if UserInfo.containsAnyProfileField(profile_fields, UserInfo.USER_PROPERTIES):
                user_props = self._stream.readValue(MultiTypeMapDatatype.RPC_DATATYPE)
                if isinstance(user_props, MultiTypeMap):
                    info.userProperties = user_props
                else:
                    info.userProperties = None
        except (EOFError, ValueError):
            # Truncated or malformed payloads appear in certain dumps; return
            # the partially populated structure rather than failing entirely.
            return info

        return info

    def readQuestTracker(self) -> RpcQuestTracker:
        tracker = RpcQuestTracker()
        tracker.questId = self._stream.readUintvar31()
        tracker.stepsCompleted = self._stream.readUintvar31()
        return tracker

    def readRewardTracker(self) -> RpcRewardTracker:
        tracker = RpcRewardTracker()
        tracker.rewardId = self._stream.readUintvar31()
        tracker.timesAwardedToday = self._stream.readUintvar31()
        return tracker

    def readOwnedItem(self) -> RpcOwnedItem:
        item = RpcOwnedItem()
        item.itemId = self._stream.readIntvar32()
        item.itemHash = self._stream.readUintvar32()
        item.active = self._stream.readBoolean()
        item.roomIndex = self._stream.readUintvar31()
        item.positionX = self._stream.readIntvar32()
        item.positionY = self._stream.readIntvar32()
        item.positionZ = self._stream.readIntvar32()
        item.createTime = self._stream.readDate()
        item.containedItem = self._stream.readUintvar32()
        item.containedItem2 = self._stream.readUintvar32()
        item.containedType = self._stream.readUintvar32()
        item.containedAmount = self._stream.readUintvar32()
        item.sender = self.readNetworkUid()
        item.message = self._stream.readString()
        item.itemProperties = self._stream.readValue(MultiTypeMapDatatype.RPC_DATATYPE)
        item.containedItemProperties = self._stream.readValue(
            MultiTypeMapDatatype.RPC_DATATYPE
        )
        item.containedItem2Properties = self._stream.readValue(
            MultiTypeMapDatatype.RPC_DATATYPE
        )
        return item

    def readAuditChangeBatch(self) -> AuditChangeBatch:
        change_batch = AuditChangeBatch()

        change_batch.saveVersion = self._stream.readUintvar31()
        change_batch.auditChanges = self._stream.readArray(self.readAuditChange)
        change_batch.visitedUids = self._stream.readArray(self.readNetworkUid)

        return change_batch

    def readAuditChange(self) -> AuditChange:
        s = self._stream
        change = AuditChange()

        change.action = s.readUint8()
        change.newCredits = s.readUintvar31()
        change.newRecyclePoints = s.readUintvar31()
        change.newStickerPoints = s.readUintvar31()
        change.creditsDelta = s.readIntvar32()
        change.token = s.readString()
        change.newItemId = s.readIntvar32()
        change.itemId = s.readIntvar32()
        change.itemHash = s.readUintvar32()
        change.active = s.readBoolean()
        change.roomIndex = s.readUintvar31()
        change.positionX = s.readIntvar32()
        change.positionY = s.readIntvar32()
        change.positionZ = s.readIntvar32()
        change.createTime = s.readDate()
        change.containedItem = s.readUintvar32()
        change.containedType = s.readUintvar31()
        change.containedAmount = s.readUintvar31()
        change.sender = self.readNetworkUid()
        change.message = s.readString()
        change.accompanyingItemId = s.readIntvar32()
        change.csum = s.readUint8()

        return change

    def readFeedLink(self) -> FeedLink:
        link = FeedLink()
        link.itemHash = self._stream.readUintvar32()
        link.recipients = self._stream.readArray(self.readFeedLinkRecipient)
        link.creationDate = self._stream.readDate()
        link.rewardClaimed = self._stream.readBoolean()
        return link

    def readFeedLinkRecipient(self) -> FeedLinkRecipient:
        recipient = FeedLinkRecipient()
        recipient.recipient = self.readNetworkUid()
        recipient.clickedDate = self._stream.readDate()
        return recipient

    def readLimitedItem(self) -> Optional[LimitedItem]:
        is_null = self._stream.readBoolean()
        if is_null:
            return None
        item = LimitedItem()
        item.itemHash = self._stream.readUintvar32()
        item.amountSold = self._stream.readUintvar31()
        item.amountForSale = self._stream.readUintvar31()
        item.soldDate = self._stream.readDate()
        item.dailyPurchaseLimit = self._stream.readUintvar31()
        item.isCashItem = self._stream.readBoolean()
        return item

    def readNewHouseData(self) -> Optional[Dict[str, Any]]:
        _ = self._stream.readUintvar31()
        is_null = self._read_relaxed_boolean(default=False)
        if is_null:
            return None
        return {
            "cashRoomsCount": self._stream.readUintvar31(),
            "cashGardensCount": self._stream.readUintvar31(),
            "itemHash": self._stream.readUintvar32(),
        }

    def readCollaborativeBuildItem(self) -> Optional[RpcCollaborativeBuildItem]:
        _ = self._stream.readUintvar31()
        is_null = self._stream.readBoolean()
        if is_null:
            return None
        item = RpcCollaborativeBuildItem()
        item.itemID = self._stream.readUintvar32()
        count = self._stream.readUintvar31()
        for _ in range(count):
            component_id = self._stream.readUintvar32()
            component_count = self._stream.readUintvar31()
            item.setCount(component_id, component_count)
        return item

    def readDailyBonusInformation(self) -> Dict[str, int]:
        return {
            "cashAmount": self._stream.readUintvar31(),
            "coinAmount": self._stream.readUintvar31(),
            "item": self._stream.readUintvar32(),
            "contained": self._stream.readUintvar32(),
            "cashShovels": self._stream.readUintvar31(),
            "coinShovels": self._stream.readUintvar31(),
            "questCollectable": self._stream.readUintvar31(),
        }

    def readMiniGameItem(self) -> Optional[RpcMiniGame]:
        _ = self._stream.readUintvar31()
        is_null = self._stream.readBoolean()
        if is_null:
            return None
        mini_game = RpcMiniGame()
        mini_game.gameID = self._stream.readUintvar32()
        mini_game.triesLeft = self._stream.readUintvar32()
        count = self._stream.readUintvar31()
        for _ in range(count):
            element_id = self._stream.readUintvar32()
            value = self._stream.readUintvar32()
            mini_game.setElementValue(element_id, value)
        return mini_game

    def readDIYBuildItem(self) -> Optional[RpcDIYBuildItem]:
        _ = self._stream.readUintvar31()
        is_null = self._stream.readBoolean()
        if is_null:
            return None
        diy_item = RpcDIYBuildItem()
        diy_item.itemID = self._stream.readUintvar32()
        count = self._stream.readUintvar31()
        for _ in range(count):
            component_id = self._stream.readUintvar32()
            timestamp = self._stream.readFloat64()
            diy_item.setTimeStamp(component_id, timestamp)
        return diy_item

    def readWeeklyQuestData(self) -> Optional[RpcWeeklyQuest]:
        _ = self._stream.readUintvar31()
        is_null = self._stream.readBoolean()
        if is_null:
            return None
        quest = RpcWeeklyQuest()
        quest.questID = self._stream.readUintvar32()
        quest.reward = self._stream.readUintvar32()
        quest.graceHours = self._stream.readUintvar32()
        return quest

    def readQuestActivityData(self) -> Optional[Dict[str, Any]]:
        _ = self._stream.readUintvar31()
        is_null = self._stream.readBoolean()
        if is_null:
            return None
        return {
            "questID": self._stream.readUintvar32(),
            "subQuestID": self._stream.readUintvar32(),
            "count": self._stream.readUintvar32(),
            "reward": self._stream.readString(),
        }

    def readBuilderQuestActivity(self) -> Optional[Dict[str, Any]]:
        _ = self._stream.readUintvar31()
        is_null = self._stream.readBoolean()
        if is_null:
            return None
        quest_data: Dict[str, Any] = {}
        quest_data["questID"] = self._stream.readUintvar32()
        quest_data["activityID"] = self._stream.readUintvar32()
        collectable = BuilderCollectable()
        collectable.id = self._stream.readUintvar32()
        collectable.currentCount = self._stream.readUintvar32()
        quest_data["activityStatus"] = self._stream.readUintvar32()
        collectable.requestDate = self._stream.readDate()
        collectable.activityStatus = quest_data["activityStatus"]
        quest_data["collectable"] = collectable
        return quest_data

    def readBuilderQuestData(self) -> Optional[Dict[str, Any]]:
        _ = self._stream.readUintvar31()
        is_null = self._stream.readBoolean()
        if is_null:
            return None
        return {
            "questID": self._stream.readUintvar32(),
            "reward": self._stream.readUintvar32(),
            "graceHours": self._stream.readUintvar32(),
        }

    def readBuildProgressData(self) -> Optional[Dict[str, Any]]:
        _ = self._stream.readUintvar31()
        is_null = self._stream.readBoolean()
        if is_null:
            return None
        return {
            "questID": self._stream.readUintvar32(),
            "activityID": self._stream.readUintvar32(),
            "collectableID": self._stream.readUintvar32(),
            "startTime": self._stream.readFloat64(),
            "endTime": self._stream.readFloat64(),
        }

    def mergeBuildQuestData(self, *sources: List[Any]) -> List[Any]:
        merged: List[Any] = []
        for source in sources:
            if isinstance(source, list):
                for entry in source:
                    if entry not in merged:
                        merged.append(entry)
        return merged

    def _read_relaxed_boolean(self, default: bool = False) -> bool:
        stream = self._stream
        if stream is None:
            return default
        if not hasattr(stream, "_input"):
            return stream.readBoolean()

        checkpoint = stream._input.tell()
        try:
            return stream.readBoolean()
        except ValueError:
            stream._input.seek(checkpoint)
            return default

    def readBitSet(self) -> BitSet:
        bitset = BitSet()
        bitset.setArray(self._stream.readByteArray())
        return bitset

    def readNetworkUid(self) -> Optional[NetworkUid]:
        network = self._stream.readUintvar31()
        if network == 0:
            return None
        network_uid = self._stream.readString()
        playfish_uid = self._stream.readUintvar31()
        return NetworkUid(network, network_uid, playfish_uid)

