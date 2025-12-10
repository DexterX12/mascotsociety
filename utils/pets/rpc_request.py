from __future__ import annotations

from typing import Any, Callable, Sequence

from ..datastream.output_data_stream import OutputDataStream
from ..datatypes import MultiTypeMapDatatype
from ..share import BitSet, NetworkUid
from .types import (
    AuditChange,
    AuditChangeBatch,
    DailyBonusInfo,
    FeedLink,
    FeedLinkRecipient,
    RpcCounterEvent,
    RpcOwnedItem,
    RpcQuestTracker,
)
from .user_info import UserInfo


class RpcRequest:
    """Helper methods to write bytes using user data"""

    def __init__(self, stream: OutputDataStream) -> None:
        self._stream = stream

    def __getattr__(self, name: str) -> Any:
        return getattr(self._stream, name)

    def writeUserInfo(self, user_info: UserInfo) -> None:
        s = self._stream
        self.writeNetworkUid(user_info.id)
        s.writeUintvar31(user_info.profileFields)

        if UserInfo.containsAnyProfileField(user_info.profileFields, UserInfo.FACEBOOK_INFO):
            s.writeString(user_info.usernameShort)
            s.writeString(user_info.usernameFull)
            s.writeString(user_info.imageUrl)
            s.writeString(user_info.profileUrl)

        if UserInfo.containsAnyProfileField(user_info.profileFields, UserInfo.SCORE_AND_STATS):
            s.writeBoolean(user_info.unavailable)
            s.writeString(user_info.petName)
            s.writeUintvar31(user_info.credits)
            s.writeUintvar31(user_info.petPoints)
            s.writeUint8(user_info.petLevel)
            s.writeUint8(user_info.health)
            s.writeUint8(user_info.happiness)
            s.writeUint8(user_info.hygiene)
            s.writeUintvar31(user_info.primaryColour)
            s.writeUint8(user_info.preferencesMask)
            self.writeBitSet(user_info.achievementsMask)
            s.writeDate(user_info.lastSaveTime)
            s.writeDate(user_info.lastVisitTime)
            s.writeUintvar31(user_info.streetPosition)
            s.writeUintvar31(user_info.recyclePoints)
            s.writeUintvar31(user_info.totalRecyclePoints)
            s.writeUintvar31(user_info.stickerPoints)
            s.writeUintvar31(user_info.totalStickerPoints)
            s.writeString(user_info.status)
            s.writeUint8(user_info.extraRooms)
            s.writeUint8(user_info.defaultRoomIndex)
            s.writeUintvar31(user_info.highScoreBall)
            s.writeUintvar31(user_info.highScoreFrisbee)
            s.writeUintvar31(user_info.highScoreJumpRope)
            s.writeUintvar31(user_info.numHatsBought)
            s.writeUintvar31(user_info.numShirtsBought)
            s.writeUintvar31(user_info.numTrousersBought)
            s.writeUintvar31(user_info.numShoesBought)
            s.writeUintvar31(user_info.numArmAccessoriesBought)
            s.writeUintvar31(user_info.numGiftsSent)
            s.writeUintvar31(user_info.numCoinsSpent)
            s.writeUintvar31(user_info.numVisit)
            s.writeUintvar31(user_info.numArenaHurdlesRaceWins)
            s.writeUintvar31(user_info.numArenaHurdlesBetWins)
            s.writeUintvar31(user_info.numProHurdlesRaceWins)
            s.writeUintvar31(user_info.numPlantsGrown)
            s.writeUintvar31(user_info.coinsWon)
            s.writeUintvar31(user_info.cookingPoints)
            self.writeBitSet(user_info.recipesMask)
            s.writeDate(user_info.petBirthday)
            s.writeUintvar31(user_info.playCount)
            s.writeUintvar31(user_info.coinShovels)
            s.writeUintvar31(user_info.cashShovels)
            s.writeIntvar32(user_info.plotTopLeftX)
            s.writeIntvar32(user_info.plotTopLeftY)
            s.writeIntvar32(user_info.plotBottomRightX)
            s.writeIntvar32(user_info.plotBottomRightY)

        if UserInfo.containsAnyProfileField(user_info.profileFields, UserInfo.OWNED_ITEMS, UserInfo.OWNED_EXTERIOR_ITEMS):
            owned_items = user_info.ownedItems or []
            s.writeArray(owned_items, self.writeOwnedItem)

        if UserInfo.containsAnyProfileField(user_info.profileFields, UserInfo.INACTIVE_ITEMS):
            completed_sets = user_info.completedSets or []
            s.writeArray(completed_sets, s.writeUintvar32)
            self.writeBitSet(user_info.tutorialMask)
            s.writeUintvar31(user_info.newsletterIndex)
            s.writeUintvar31(user_info.numArenaHurdlesRacesLeftToday)
            s.writeUintvar31(user_info.numProHurdlesRacesLeftToday)
            s.writeUintvar31(user_info.dailyArenaHurdlesBetProfit)
            s.writeUintvar31(user_info.checkoutVersion)
            s.writeDate(user_info.lastPurchaseTime)
            s.writeDate(user_info.lastBookmarkPopupTime)
            s.writeUintvar31(user_info.consecutiveLoginDays)
            s.writeDate(user_info.lastLotteryTime)

        if UserInfo.containsAnyProfileField(user_info.profileFields, UserInfo.TRACKING_INFO):
            quest_trackers = user_info.questTrackers or []
            s.writeArray(quest_trackers, self.writeQuestTracker)

        if UserInfo.containsAnyProfileField(user_info.profileFields, UserInfo.USER_PROPERTIES):
            s.writeValue(MultiTypeMapDatatype.RPC_DATATYPE, user_info.userProperties)

    def writeOwnedItem(self, item: RpcOwnedItem) -> None:
        s = self._stream
        s.writeIntvar32(item.itemId)
        s.writeUintvar32(item.itemHash)
        s.writeBoolean(item.active)
        s.writeUintvar31(item.roomIndex)
        s.writeIntvar32(item.positionX)
        s.writeIntvar32(item.positionY)
        s.writeIntvar32(item.positionZ)
        s.writeDate(item.createTime)
        s.writeUintvar32(item.containedItem)
        s.writeUintvar32(item.containedItem2)
        s.writeUintvar32(item.containedType)
        s.writeUintvar32(item.containedAmount)
        self.writeNetworkUid(item.sender)
        s.writeString(item.message)
        s.writeValue(MultiTypeMapDatatype.RPC_DATATYPE, item.itemProperties)
        s.writeValue(MultiTypeMapDatatype.RPC_DATATYPE, item.containedItemProperties)
        s.writeValue(MultiTypeMapDatatype.RPC_DATATYPE, item.containedItem2Properties)

    def writeQuestTracker(self, tracker: RpcQuestTracker) -> None:
        s = self._stream
        s.writeUintvar31(tracker.questId)
        s.writeUintvar31(tracker.stepsCompleted)

    def writeFeedLinkRecipient(self, recipient: FeedLinkRecipient) -> None:
        self.writeNetworkUid(recipient.recipient)
        self._stream.writeDate(recipient.clickedDate)

    def writeFeedLink(self, link: FeedLink) -> None:
        s = self._stream
        s.writeUintvar32(link.itemHash)
        recipients = link.recipients or []
        s.writeArray(recipients, self.writeFeedLinkRecipient)
        s.writeDate(link.creationDate)
        s.writeBoolean(link.rewardClaimed)

    def writeDailyBonusInfo(self, info: DailyBonusInfo | None) -> None:
        info = info or DailyBonusInfo()
        s = self._stream
        s.writeBoolean(info.isDailyBonusEnabled)
        if info.isDailyBonusEnabled:
            s.writeBoolean(info.canClaimDailyBonus)
            s.writeUint8(info.dailyBonusDay)

    def writeVersionArray(self, version: int, values: Sequence[Any], writer: Callable[[Any], None]) -> None:
        self._stream.writeUintvar31(version)
        self._stream.writeArray(values, writer)

    def writeRpcCounterEvent(self, event: RpcCounterEvent) -> None:
        self.writeNetworkUid(event.userID)
        self._stream.writeUintvar31(event.counterEventID)
        self._stream.writeUintvar31(event.aggregateID)
        self._stream.writeUintvar31(event.eventType)
        self._stream.writeDate(event.triggerDate)
        self._stream.writeUintvar31(event.eventStatus)
        self.writeNetworkUid(event.senderID)
        self._stream.writeString(event.eventData)

    def writePurchaseDetails(self, details: Sequence[Any]) -> None:
        s = self._stream
        s.writeString(str(details[0]))
        s.writeString(str(details[1]))
        s.writeIntvar32(int(details[2]))
        s.writeString(str(details[3]))
        s.writeUintvar32(int(details[4]))
        s.writeIntvar32(int(details[5]))
        s.writeIntvar32(int(details[6]))
        s.writeIntvar32(int(details[7]))

    def writeNetworkUid(self, uid: NetworkUid | None) -> None:
        s = self._stream
        if uid is None:
            s.writeUintvar31(0)
            return
        s.writeUintvar31(uid._network)
        s.writeString(uid._networkUid)
        s.writeUintvar31(uid._playfishUid)

    def writeBitSet(self, bitset: BitSet | None) -> None:
        if bitset is None:
            self._stream.writeByteArray(b"")
        else:
            self._stream.writeByteArray(bitset.bits)

    def writeNewHouseData(self, new_house_data: dict) -> None:
        self._stream.writeUintvar31(100)
        self._stream.writeBoolean(False)
        self._stream.writeUintvar31(new_house_data["cashRoomsCount"])
        self._stream.writeUintvar31(new_house_data["cashGardensCount"])
        self._stream.writeUintvar32(new_house_data["itemHash"])
        

    def getvalue(self) -> bytes:
        return self._stream.getvalue()