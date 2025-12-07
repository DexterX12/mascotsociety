from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

from ...utils.pets.types import RpcOwnedItem

from ..datatypes import MultiTypeMap
from ..share import BitSet, NetworkUid


@dataclass
class UserInfo:
    TOTAL_OWNED_ITEM_LIMIT: int = 10000

    FACEBOOK_INFO: int = 1
    SCORE_AND_STATS: int = 2
    OWNED_ITEMS: int = 4
    INACTIVE_ITEMS: int = 8
    OWNED_EXTERIOR_ITEMS: int = 16
    TRACKING_INFO: int = 32
    USER_PROPERTIES: int = 64

    PROFILE_CLASS_2: int = 3
    PROFILE_CLASS_4: int = 7
    PROFILE_CLASS_5: int = 47

    id: Optional[NetworkUid] = None
    profileFields: int = 0
    usernameShort: str = ""
    usernameFull: str = ""
    imageUrl: str = ""
    image: Optional[list] = None
    profileUrl: str = ""
    unavailable: bool = False
    coinsWon: int = 0
    petName: str = ""
    credits: int = 0
    petPoints: int = 0
    petLevel: int = 0
    health: int = 0
    happiness: int = 0
    hygiene: int = 0
    primaryColour: int = 0
    secondaryColour: int = 0
    preferencesMask: int = 0
    achievementsMask: Optional[BitSet] = None
    lastSaveTime: Optional[datetime] = None
    lastVisitTime: Optional[datetime] = None
    streetPosition: int = 0
    recyclePoints: int = 0
    totalRecyclePoints: int = 0
    stickerPoints: int = 0
    totalStickerPoints: int = 0
    consecutiveLoginDays: int = 0
    lastLotteryTime: Optional[datetime] = None
    status: str = ""
    defaultRoomIndex: int = 0
    extraRooms: int = 0
    ownedItems: Optional[list] = None
    completedSets: Optional[list] = None
    tutorialMask: Optional[BitSet] = None
    newsletterIndex: int = 0
    highScoreBall: int = 0
    highScoreFrisbee: int = 0
    highScoreJumpRope: int = 0
    numHatsBought: int = 0
    numShirtsBought: int = 0
    numTrousersBought: int = 0
    numShoesBought: int = 0
    numArmAccessoriesBought: int = 0
    numGiftsSent: int = 0
    numCoinsSpent: int = 0
    numVisit: int = 0
    numArenaHurdlesRaceWins: int = 0
    numArenaHurdlesBetWins: int = 0
    numArenaHurdlesRacesLeftToday: int = 0
    numProHurdlesRaceWins: int = 0
    numProHurdlesRacesLeftToday: int = 0
    dailyArenaHurdlesBetProfit: int = 0
    numPlantsGrown: int = 0
    checkoutVersion: int = 0
    lastPurchaseTime: Optional[datetime] = None
    lastBookmarkPopupTime: Optional[datetime] = None
    cookingPoints: int = 0
    recipesMask: Optional[BitSet] = None
    petBirthday: Optional[datetime] = None
    playCount: int = 0
    coinShovels: int = 0
    cashShovels: int = 0
    plotTopLeftX: int = 0
    plotTopLeftY: int = 0
    plotBottomRightX: int = 0
    plotBottomRightY: int = 0
    questTrackers: Optional[list] = None
    userProperties: Optional[MultiTypeMap] = None

    @staticmethod
    def containsAnyProfileField(profile_fields: int, *fields: int) -> bool:
        for flag in fields:
            if (profile_fields & flag) == flag:
                return True
        return False

    @staticmethod
    def containsAllProfileField(profile_fields: int, *fields: int) -> bool:
        for flag in fields:
            if (profile_fields & flag) != flag:
                return False
        return True
        
    def getItemIndexById(self, itemId:int) -> int:
        for i in range(len(self.ownedItems)):
            if not self.ownedItems[i].itemId == itemId: continue
            return i
        return -1

    def __str__(self) -> str:
        parts = [f"[UserInfo: id={self.id} profileClass={self.profileFields} unavailable={self.unavailable}"]
        if UserInfo.containsAnyProfileField(self.profileFields, UserInfo.FACEBOOK_INFO):
            parts.append(
                f" usernameShort=\"{self.usernameShort}\""
                f" usernameFull=\"{self.usernameFull}\""
                f" imageUrl=\"{self.imageUrl}\""
            )
        if UserInfo.containsAnyProfileField(self.profileFields, UserInfo.SCORE_AND_STATS):
            parts.append(
                f" petName=\"{self.petName}\" credits={self.credits} recyclePoints={self.recyclePoints}"
                f" totalRecyclePoints={self.totalRecyclePoints} stickerPoints={self.stickerPoints}"
                f" totalStickerPoints={self.totalStickerPoints} status=\"{self.status}\""
                f" extraRooms={self.extraRooms} petPoints={self.petPoints} petLevel={self.petLevel}"
                f" health={self.health} happiness={self.happiness} hygiene={self.hygiene}"
                f" primaryColour={self.primaryColour} secondaryColour={self.secondaryColour}"
                f" preferencesMask={self.preferencesMask} achievementsMask={self.achievementsMask}"
                f" lastSaveTime={self.lastSaveTime} lastVisitTime={self.lastVisitTime}"
                f" streetPosition={self.streetPosition} defaultRoomIndex={self.defaultRoomIndex}"
                f" highScoreBall={self.highScoreBall} highScoreFrisbee={self.highScoreFrisbee}"
                f" highScoreJumpRope={self.highScoreJumpRope} numHatsBought={self.numHatsBought}"
                f" numShirtsBought={self.numShirtsBought} numTrousersBought={self.numTrousersBought}"
                f" numShoesBought={self.numShoesBought} numArmAccessoriesBought={self.numArmAccessoriesBought}"
                f" numGiftsSent={self.numGiftsSent} numCoinsSpent={self.numCoinsSpent}"
                f" numVisit={self.numVisit} numArenaHurdlesRaceWins={self.numArenaHurdlesRaceWins}"
                f" numArenaHurdlesBetWins={self.numArenaHurdlesBetWins}"
                f" numProHurdlesRaceWins={self.numProHurdlesRaceWins} numPlantsGrown={self.numPlantsGrown}"
                f" coinsWon={self.coinsWon} cookingPoints={self.cookingPoints} recipesMask={self.recipesMask}"
                f" petBirthday={self.petBirthday} coinShovels={self.coinShovels} cashShovels={self.cashShovels}"
                f" playCount={self.playCount} userProperties={self.userProperties}"
            )
        if UserInfo.containsAnyProfileField(self.profileFields, UserInfo.INACTIVE_ITEMS):
            parts.append(
                f" tutorialMask={self.tutorialMask} numArenaHurdlesRacesLeftToday={self.numArenaHurdlesRacesLeftToday}"
                f" numProHurdlesRacesLeftToday={self.numProHurdlesRacesLeftToday}"
                f" dailyArenaHurdlesBetProfit={self.dailyArenaHurdlesBetProfit} lastPurchaseTime={self.lastPurchaseTime}"
                f" consecutiveLoginDays={self.consecutiveLoginDays} lastLotteryTime={self.lastLotteryTime}"
                f" lastBookmarkPopupTime={self.lastBookmarkPopupTime} checkoutVersion={self.checkoutVersion}"
            )
        if self.ownedItems is not None:
            parts.append(" ownedItems={")
            for item in self.ownedItems:
                parts.append(f"\n{item}")
            parts.append(" }")
        parts.append("]")
        return "".join(parts)
