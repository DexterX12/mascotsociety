from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ...utils.pets.types import RpcCollaborativeBuildItem
from ...constants import Events
from ... import database_handler

def handle_get_collaborative_build_items(stream:InputDataStream) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    requested_hashes = rpc_res.readArray(rpc_res.readUintvar32)
    component_map = database_handler.collaborative_items
    items = []

    for item_hash in requested_hashes:
        collab_item = RpcCollaborativeBuildItem()
        collab_item.itemID = item_hash

        for component_id in component_map.get(item_hash, []):
            collab_item.setCount(component_id, 0)

        items.append(collab_item)

    rpc_req.writeUintvar31(Events.ITEM_INFO_FOUND)
    rpc_req.writeArray(items, rpc_req.writeCollaborativeBuildItem)

    return response.getvalue()
