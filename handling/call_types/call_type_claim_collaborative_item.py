from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ...constants import Events
from ... import database_handler, profile_handler

def handle_claim_collaborative_item(stream:InputDataStream) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    item = {
        "itemHash": rpc_res.readUintvar32()
    }

    created_collaborative_item = profile_handler.create_item({
        "itemHash": item["itemHash"]
    })

    rpc_req.writeUintvar31(Events.ITEM_CLAIMED)
    rpc_req.writeIntvar32(created_collaborative_item.itemId)
    rpc_req.writeUintvar32(created_collaborative_item.itemHash)
    rpc_req.writeUintvar32(created_collaborative_item.containedItem)

    return response.getvalue()
