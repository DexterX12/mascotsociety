from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ...utils.pets.types import RpcOwnedItem
from ...utils.hash import hashInt32
from ... import profile_handler
from ... import database_handler
from ...constants import Events

def handle_purchase_multiple_cash_or_coin_items(stream:InputDataStream) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    purchase_data = {
        "networkUid": rpc_res.readNetworkUid(),
        "boughtCashItems": rpc_res.readArray(rpc_res.readPurchaseDetails),
        "boughtCreditsItems": rpc_res.readArray(rpc_res.readPurchaseDetails)
    }

    item_group = [purchase_data["boughtCashItems"], purchase_data["boughtCreditsItems"]]
    cash_delta = 0
    credit_delta = 0
    final_status = Events.PURCHASE_CASH_OK
    bought_items = []

    for i in range(2):
        for item in item_group[i]:
            purchased_item = database_handler.findItemByToken(item["token"])
            
            new_rpc_item = RpcOwnedItem()

            new_rpc_item.itemId = abs(item["itemId"])
            new_rpc_item.itemHash = purchased_item["itemHash"]
            new_rpc_item.containedType = item["containedItemHash"]
            new_rpc_item.positionX = item["positionX"]
            new_rpc_item.positionY = item["positionY"]
            new_rpc_item.positionZ = item["positionZ"]

            bought_items.append(new_rpc_item)

            if i == 0:
                cash_delta += int(purchased_item["cost"])
            else:
                credit_delta += int(purchased_item["cost"])

    if cash_delta > profile_handler.cash:
        final_status = Events.PURCHASE_CASH_FAIL_NOT_ENOUGH_GAME_CURRENCY
    else:
        profile_handler.cash -= cash_delta
        profile_handler.user.credits -= credit_delta

        profile_handler.user.ownedItems.extend(bought_items)

    rpc_req.writeUintvar31(final_status)
    rpc_req.writeIntvar32(cash_delta * -1)
    rpc_req.writeIntvar32(credit_delta * -1)

    return response.getvalue()
