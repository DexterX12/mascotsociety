import profile
from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ...utils.pets.types import RpcOwnedItem
from ...utils.hash import hashInt32
from ... import profile_handler
from ... import database_handler
from ...constants import Events, ContainedTypes
from ...constants.mystery import Mystery
from random import choice

def handle_redeem_voucher(stream:InputDataStream) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    item_id = rpc_res.readIntvar32()
    max_item_id = max(item.itemId for item in profile_handler.user.ownedItems)
    
    item_index = profile_handler.user.getItemIndexById(item_id)

    if item_index == -1:
        print("Not found item with id =",item_id)
        rpc_req.writeUintvar31(Events.REDEEM_VOUCHER_DOES_NOT_EXIST)
        return b''
    
    
    item = profile_handler.user.ownedItems[item_index]
    
        
        
    
    return response.getvalue()
