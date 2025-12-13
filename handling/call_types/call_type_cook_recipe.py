from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ...constants import Events, Recipes, ContainedTypes
from ... import database_handler, profile_handler
from datetime import datetime, timezone

from random import choice

def handle_cook_recipe(stream:InputDataStream) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    recipe_details = {
        "token": rpc_res.readString(), # Stove
        "recipeId": rpc_res.readIntvar32(),
        "itemId": rpc_res.readIntvar32(),
        "checkoutVersion": rpc_res.readUintvar31()
    }

    profile_handler.update_item({
        "audit": False,
        "itemId": recipe_details["itemId"],
        "createTime": datetime.now(timezone.utc),
        "containedType": ContainedTypes.CONTAINED_CRAFTING_DEVICE,
        "containedItem": Recipes.HASHES[recipe_details["recipeId"]]
    })

    rpc_req.writeUintvar31(Events.START_CRAFTING_STATUS_OK)
    return response.getvalue()