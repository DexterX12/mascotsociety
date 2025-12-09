from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ... import profile_handler
from ... import database_handler
from ...constants import Events
from ...constants.mystery import Redeemable
from ...utils.pets.types import RpcOwnedItem

def handle_redeem_voucher(stream:InputDataStream) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    itemIds = []
    itemHashes = []
    itemContainedType = []
    itemContainedType2 = []

    item_id = abs(rpc_res.readIntvar32())
    item_index = profile_handler.user.getItemIndexById(item_id)

    if item_index == -1:
        print("Not found item with id =",item_id)
        rpc_req.writeUintvar31(Events.REDEEM_VOUCHER_DOES_NOT_EXIST)
        return b''

    voucher_owned_item = profile_handler.user.ownedItems.pop(item_index)
    max_item_id = max(item.itemId for item in profile_handler.user.ownedItems)
    voucher_item = database_handler.findItemByHash(voucher_owned_item.itemHash)
    voucher_rewards = getattr(Redeemable, voucher_item["name"].replace(" ", "_").upper(), [])

    for reward in voucher_rewards:
        item_reward = database_handler.findItemByName(reward)

        itemIds.append(max_item_id + 1)
        itemHashes.append(item_reward["itemHash"])
        itemContainedType.append(0)
        itemContainedType2.append(0)

        ownedItem = RpcOwnedItem()
        ownedItem.itemId = max_item_id + 1
        ownedItem.itemHash = item_reward["itemHash"]

        profile_handler.user.ownedItems.append(ownedItem)

        max_item_id += 1

    rpc_req.writeUintvar31(Events.REDEEM_VOUCHER_SUCCESS)
    rpc_req.writeArray(itemIds, rpc_req.writeIntvar32)
    rpc_req.writeArray(itemHashes, rpc_req.writeUintvar32)
    rpc_req.writeArray(itemContainedType, rpc_req.writeUintvar32)
    rpc_req.writeArray(itemContainedType2, rpc_req.writeUintvar32)
    
    return response.getvalue()
