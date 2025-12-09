from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ...utils.pets.types import RpcOwnedItem
from ...utils.hash import hashInt32
from ... import profile_handler
from ... import database_handler
from ...constants import Events

def handle_exchange_cash_for_coins(stream:InputDataStream) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    purchase_data = {
        "token": rpc_res.readString()
    }

    purchased_coinbag = database_handler.findItemByToken(purchase_data["token"])
    profile_handler.cash -= int(purchased_coinbag["cost"])
    profile_handler.user.credits += int(purchased_coinbag["sellValue"])
    
    rpc_req.writeUintvar31(Events.PURCHASE_CASH_OK)
    rpc_req.writeUintvar31(profile_handler.cash)

    return response.getvalue()
