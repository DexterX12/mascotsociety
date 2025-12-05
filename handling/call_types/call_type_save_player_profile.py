from datetime import datetime, time, timezone
from utils.datastream.output_data_stream import OutputDataStream
from utils.datastream.input_data_stream import InputDataStream
from utils.datatypes import MultiTypeMapDatatype
from utils.pets.rpc_request import RpcRequest
from utils.pets.rpc_response import RpcResponse
from constants import EVENTS, type_to_int
from utils.pets.types import DailyBonusInfo
from utils.datatypes import MultiTypeMapDatatype

def place_data_in_profile(client_info: RpcResponse, context:dict):
    context["profile"].user.petName = client_info.readString()
    context["profile"].user.credits = client_info.readUintvar31()
    context["profile"].user.recyclePoints = client_info.readUintvar31()
    context["profile"].user.totalRecyclePoints = client_info.readUintvar31()
    context["profile"].user.stickerPoints = client_info.readUintvar31()
    context["profile"].user.totalStickerPoints = client_info.readUintvar31()
    context["profile"].user.status = client_info.readString()
    context["profile"].user.petPoints = client_info.readUintvar31()
    context["profile"].user.petLevel = client_info.readUint8()
    context["profile"].user.health = client_info.readUint8()
    context["profile"].user.happiness = client_info.readUint8()
    context["profile"].user.hygiene = client_info.readUint8()
    context["profile"].user.primaryColour = client_info.readUintvar31()
    context["profile"].user.preferencesMask = client_info.readUint8()
    context["profile"].user.achievementsMask = client_info.readBitSet()
    context["profile"].user.tutorialMask = client_info.readBitSet()
    context["profile"].user.newsletterIndex = client_info.readUintvar31()
    context["profile"].user.highScoreBall = client_info.readUintvar31()
    context["profile"].user.highScoreFrisbee = client_info.readUintvar31()
    context["profile"].user.highScoreJumpRope = client_info.readUintvar31()
    context["profile"].user.numHatsBought = client_info.readUintvar31()
    context["profile"].user.numShirtsBought = client_info.readUintvar31()
    context["profile"].user.numTrousersBought = client_info.readUintvar31()
    context["profile"].user.numShoesBought = client_info.readUintvar31()
    context["profile"].user.numArmAccessoriesBought = client_info.readUintvar31()
    context["profile"].user.numGiftsSent = client_info.readUintvar31()
    context["profile"].user.numCoinsSpent = client_info.readUintvar31()
    context["profile"].user.numVisit = client_info.readUintvar31()
    context["profile"].user.numArenaHurdlesRaceWins = client_info.readUintvar31()
    context["profile"].user.numArenaHurdlesBetWins = client_info.readUintvar31()
    context["profile"].user.numArenaHurdlesRacesLeftToday = client_info.readUintvar31()
    context["profile"].user.numProHurdlesRaceWins = client_info.readUintvar31()
    context["profile"].user.numProHurdlesRacesLeftToday = client_info.readUintvar31()
    context["profile"].user.dailyArenaHurdlesBetProfit = client_info.readUintvar31()
    context["profile"].user.numPlantsGrown = client_info.readUintvar31()
    context["profile"].user.checkoutVersion = client_info.readUintvar31()
    context["profile"].user.extraRooms = client_info.readUint8()
    context["profile"].user.defaultRoomIndex = client_info.readUint8()
    context["profile"].user.lastBookmarkPopupTime = client_info.readDate()
    context["profile"].user.cookingPoints = client_info.readUintvar31()
    context["profile"].user.recipesMask = client_info.readBitSet()
    context["profile"].user.petBirthday = client_info.readDate()
    context["profile"].user.playCount = client_info.readUintvar31()
    context["profile"].user.coinShovels = client_info.readUintvar31()
    context["profile"].user.cashShovels = client_info.readUintvar31()
    context["profile"].user.userProperties = client_info.readValue(MultiTypeMapDatatype.RPC_DATATYPE)
    context["profile"].user.lastSaveTime = datetime.now(timezone.utc)

def handle_save_player_profile(stream:InputDataStream, context={}) -> bytes:
    client_info = RpcResponse(stream)
    response = RpcRequest(OutputDataStream())

    place_data_in_profile(client_info, context)

    client_info.readUint8()
    client_info.readUint8()
    client_info.readUint8()
    client_info.readUint8()

    audited_changes = client_info.readArray(client_info.readAuditChangeBatch)

    print("Changes to audit: ", len(audited_changes))
    for batch_change in audited_changes:
        print("Batch of audit changes:", len(batch_change.auditChanges))
        for change in batch_change.auditChanges:
            print(change, "\n")
        print(audited_changes[0].saveVersion, "\n\n\n\n")



    response.writeUintvar31(type_to_int(EVENTS, "SAVE_STATUS_OK"))
    response.writeUintvar32(0)
    response.writeBoolean(0)
    response.writeDailyBonusInfo(DailyBonusInfo())
    response.writeUintvar31(audited_changes[0].saveVersion)
    response.writeArray([], response.writeOwnedItem)
    response.writeUintvar31(0)
    response.writeUintvar31(0)

    return response.getvalue()