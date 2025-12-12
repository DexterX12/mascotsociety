import profile
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
    
    voucher_owned_item = profile_handler.delete_item({
        "itemId": item_id
    })

    voucher_item = database_handler.find_item_by_hash(voucher_owned_item.itemHash)
    voucher_rewards = getattr(Redeemable, voucher_item["name"].upper().replace(" ", "_"), [])

    for reward in voucher_rewards:
        item_reward = database_handler.find_item_by_name(reward)

        created_reward = profile_handler.create_item({
            "itemHash": item_reward["itemHash"]
        })

        itemIds.append(created_reward.itemId)
        itemHashes.append(created_reward.itemHash)
        itemContainedType.append(0)
        itemContainedType2.append(0)

    rpc_req.writeUintvar31(Events.REDEEM_VOUCHER_SUCCESS)
    rpc_req.writeArray(itemIds, rpc_req.writeIntvar32)
    rpc_req.writeArray(itemHashes, rpc_req.writeUintvar32)
    rpc_req.writeArray(itemContainedType, rpc_req.writeUintvar32)
    rpc_req.writeArray(itemContainedType2, rpc_req.writeUintvar32)
    
    return response.getvalue()
