from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ... import profile_handler
from ... import database_handler
from ...constants import Events
from ...constants.treasure import Treasure
from random import choice

def handle_save_digging_game(stream:InputDataStream) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    digging_details = {
        "mapId": rpc_res.readUintvar32(),
        "diggingEvent": rpc_res.readIntvar32(),
        "foundCoins": rpc_res.readArray(rpc_res.readUintvar31),
        "shovelIds": rpc_res.readArray(rpc_res.readUintvar31)
    }
    rpc_req.writeUintvar31(Events.SUCCESS)

    if digging_details["diggingEvent"] == Events.FIND_COINS_OR_NOTHING_OR_SHOVELS:
        profile_handler.user.credits += sum(digging_details["foundCoins"])

        rpc_req.writeUintvar31(0)
        rpc_req.writeUintvar32(0)
        rpc_req.writeUintvar31(0)
        rpc_req.writeUintvar32(0)
    else:
        map_treasures = Treasure.MAPPING[digging_details["mapId"]]

        if len(map_treasures) == 0:
            map_treasures = database_handler.get_non_buyable_items()
            reward_name = choice(map_treasures)["name"]
        else:
            reward_name = choice(map_treasures)
            
        reward_data = database_handler.find_item_by_name(reward_name)

        reward_item = profile_handler.create_item({
            "itemHash": reward_data["itemHash"],
        })

        rpc_req.writeUintvar31(reward_item.itemId)
        rpc_req.writeUintvar32(reward_item.itemHash)
        rpc_req.writeUintvar31(reward_item.containedType)
        rpc_req.writeUintvar32(reward_item.containedItem)

    rpc_req.writeIntvar32(profile_handler.user.credits)
    rpc_req.writeUintvar31(profile_handler.user.coinShovels)
    rpc_req.writeIntvar32(profile_handler.cash)
    rpc_req.writeUintvar31(profile_handler.user.cashShovels)

    return response.getvalue()
