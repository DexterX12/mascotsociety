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

    profile_handler.delete_item({
        "itemId": fishing_data["baitItemId"],
        "itemHash": fishing_data["baitItemHash"]
    })

    caught_item = profile_handler.create_item({
        "itemHash": fishing_data["fishItemHash"]
    })

    rpc_req.writeUintvar31(Events.FISHING_SUCCESS)
    rpc_req.writeIntvar32(caught_item.itemId)

    return response.getvalue()
