from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ...utils.pets.types import RpcOwnedItem
from ... import profile_handler
from ... import database_handler
from ...constants import Events
from datetime import datetime, timezone

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

    for i in range(len(item_group)):
        for item in item_group[i]:
            purchased_item = database_handler.find_item_by_token(item["token"])

            new_rpc_item = profile_handler.create_item({
                "itemId": abs(item["itemId"]),
                "itemHash": purchased_item["itemHash"],
                "containedItem": item["containedItemHash"],
                "positionX": item["positionX"],
                "positionY": item["positionY"],
                "positionZ": item["positionZ"]
            })

            bought_items.append(new_rpc_item)

            if i == 0:
                cash_delta += int(purchased_item["cost"])
            else:
                credit_delta += int(purchased_item["cost"])

    if cash_delta > profile_handler.cash:
        final_status = Events.PURCHASE_CASH_FAIL_NOT_ENOUGH_GAME_CURRENCY

        # highly inefficient to push and delete...
        # rework needed for better dup check
        for item in bought_items:
            profile_handler.delete_item({
                "itemId": item.itemId,
                "itemHash": item.itemHash,
                "containedItem": item.containedItem,
                "positionX": item.positionX,
                "positionY": item.positionY,
                "positionZ": item.positionZ
            })
    else:
        profile_handler.cash -= cash_delta
        profile_handler.user.credits -= credit_delta

    rpc_req.writeUintvar31(final_status)
    rpc_req.writeIntvar32(cash_delta * -1)
    rpc_req.writeIntvar32(credit_delta * -1)

    return response.getvalue()
