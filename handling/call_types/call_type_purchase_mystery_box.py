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

def handle_purchase_mystery_box(stream:InputDataStream) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    purchase_data = {
        "networkUid":rpc_res.readNetworkUid(),
        "wrapperToken": rpc_res.readString(),
        "token": rpc_res.readString(),
        "giftMessage": rpc_res.readString(),
        "amount": rpc_res.readUintvar31()
    }

    purchased_item = database_handler.findItemByToken(purchase_data["token"])

    if not purchased_item:
        print("Purchased item has not been found by its token. Token =",purchase_data["token"])
        return b''
    
    discounted_amount = purchase_data["amount"] * int(purchased_item["cost"])
    is_cash_box = "properties" in purchased_item and "cashShop" in purchased_item["properties"]
    box_owned_items = []

    if is_cash_box:
        profile_handler.cash -= discounted_amount
    else:
        profile_handler.user.credits -= discounted_amount

    for _ in range(purchase_data["amount"]):
        mystery_items = getattr(Mystery, purchased_item["name"].upper().replace(" ", "_"))
        
        # The decompiled client has the original implementation for this
        # The 'randomness' is based on item rarity, which is calculated
        # in a certain way. For simplicity, each one will have roughly the same
        # probability
        random_mystery_item = choice(mystery_items)

        mystery_item = profile_handler.create_item({
            "itemHash" : hashInt32(purchased_item["name"]),
            "containedType": ContainedTypes.CONTAINED_TREASURE,
            "containedItem": hashInt32(random_mystery_item)
        })
        
        box_owned_items.append(mystery_item)

    rpc_req.writeUintvar31(Events.MYSTERY_SUCCESS)
    rpc_req.writeUintvar31(discounted_amount)
    rpc_req.writeArray(box_owned_items, rpc_req.writeOwnedItem)
    
    return response.getvalue()
