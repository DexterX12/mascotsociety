from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ...utils.pets.types import RpcOwnedItem
from ... import profile_handler
from ...constants import Events

def handle_fishing_action(stream:InputDataStream, context={}) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    fishing_data = {
        "fishItemHash": rpc_res.readUintvar32(),
        "baitItemHash": rpc_res.readUintvar32(),
        "baitItemId": rpc_res.readIntvar32()
    }

    max_item_id = max(item.itemId for item in profile_handler.user.ownedItems)
    caught_item = RpcOwnedItem()
    caught_item.itemHash = fishing_data["fishItemHash"]
    caught_item.itemId = max_item_id + 1

    profile_handler.user.ownedItems.append(caught_item)

    rpc_req.writeUintvar31(Events.FISHING_SUCCESS)
    rpc_req.writeIntvar32(caught_item.itemId)

    print(fishing_data)

    return response.getvalue()
