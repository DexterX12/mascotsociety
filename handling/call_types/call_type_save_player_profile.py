from datetime import datetime, time, timezone
from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.datastream.input_data_stream import InputDataStream
from ...utils.datatypes import MultiTypeMapDatatype
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import RpcResponse
from ...constants import Events
from ...utils.pets.types import DailyBonusInfo
from ...utils.datatypes import MultiTypeMapDatatype
from ..audit import handle_audit
from ... import profile_handler

def place_data_in_profile(client_info: RpcResponse, context:dict):
    profile_handler.user.petName = client_info.readString()
    profile_handler.user.credits = client_info.readUintvar31()
    profile_handler.user.recyclePoints = client_info.readUintvar31()
    profile_handler.user.totalRecyclePoints  = client_info.readUintvar31()
    profile_handler.user.stickerPoints = client_info.readUintvar31()
    profile_handler.user.totalStickerPoints = client_info.readUintvar31()
    profile_handler.user.status = client_info.readString()
    profile_handler.user.petPoints = client_info.readUintvar31()
    profile_handler.user.petLevel = client_info.readUint8()
    profile_handler.user.health = client_info.readUint8()
    profile_handler.user.happiness = client_info.readUint8()
    profile_handler.user.hygiene = client_info.readUint8()
    profile_handler.user.primaryColour = client_info.readUintvar31()
    profile_handler.user.preferencesMask = client_info.readUint8()
    profile_handler.user.achievementsMask = client_info.readBitSet()
    profile_handler.user.tutorialMask = client_info.readBitSet()
    profile_handler.user.newsletterIndex = client_info.readUintvar31()
    profile_handler.user.highScoreBall = client_info.readUintvar31()
    profile_handler.user.highScoreFrisbee = client_info.readUintvar31()
    profile_handler.user.highScoreJumpRope = client_info.readUintvar31()
    profile_handler.user.numHatsBought = client_info.readUintvar31()
    profile_handler.user.numShirtsBought = client_info.readUintvar31()
    profile_handler.user.numTrousersBought = client_info.readUintvar31()
    profile_handler.user.numShoesBought = client_info.readUintvar31()
    profile_handler.user.numArmAccessoriesBought = client_info.readUintvar31()
    profile_handler.user.numGiftsSent = client_info.readUintvar31()
    profile_handler.user.numCoinsSpent = client_info.readUintvar31()
    profile_handler.user.numVisit = client_info.readUintvar31()
    profile_handler.user.numArenaHurdlesRaceWins = client_info.readUintvar31()
    profile_handler.user.numArenaHurdlesBetWins = client_info.readUintvar31()
    profile_handler.user.numArenaHurdlesRacesLeftToday = client_info.readUintvar31()
    profile_handler.user.numProHurdlesRaceWins = client_info.readUintvar31()
    profile_handler.user.numProHurdlesRacesLeftToday = client_info.readUintvar31()
    profile_handler.user.dailyArenaHurdlesBetProfit = client_info.readUintvar31()
    profile_handler.user.numPlantsGrown = client_info.readUintvar31()
    profile_handler.user.checkoutVersion = client_info.readUintvar31()
    profile_handler.user.extraRooms = client_info.readUint8()
    profile_handler.user.defaultRoomIndex = client_info.readUint8()
    profile_handler.user.lastBookmarkPopupTime = client_info.readDate()
    profile_handler.user.cookingPoints = client_info.readUintvar31()
    profile_handler.user.recipesMask = client_info.readBitSet()
    profile_handler.user.petBirthday = client_info.readDate()
    profile_handler.user.playCount = client_info.readUintvar31()
    profile_handler.user.coinShovels = client_info.readUintvar31()
    profile_handler.user.cashShovels = client_info.readUintvar31()
    profile_handler.user.userProperties = client_info.readValue(MultiTypeMapDatatype.RPC_DATATYPE)
    profile_handler.user.lastSaveTime = datetime.now(timezone.utc)

def handle_save_player_profile(stream:InputDataStream, context={}) -> bytes:
    client_info = RpcResponse(stream)
    response = RpcRequest(OutputDataStream())

    place_data_in_profile(client_info, context)

    client_info.readUint8()
    client_info.readUint8()
    client_info.readUint8()
    client_info.readUint8()

    audited_changes = client_info.readArray(client_info.readAuditChangeBatch)
    handle_audit(audited_changes)

    response.writeUintvar31(Events.SAVE_STATUS_OK)
    response.writeUintvar32(0)
    response.writeBoolean(0)
    response.writeDailyBonusInfo(DailyBonusInfo())
    response.writeUintvar31(audited_changes[0].saveVersion)
    response.writeArray([], response.writeOwnedItem)
    response.writeUintvar31(0)
    response.writeUintvar31(0)

    return response.getvalue()