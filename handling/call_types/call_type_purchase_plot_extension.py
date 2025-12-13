from ... import database_handler, profile_handler
from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ...constants import Events

def handle_purchase_plot_extension(stream:InputDataStream) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    plot_extension_details = {
        "plotTopLeftX": rpc_res.readIntvar32(),
        "plotTopLeftY": rpc_res.readIntvar32(),
        "plotBottomRightX": rpc_res.readIntvar32(),
        "plotBottomRightY": rpc_res.readIntvar32(),
        "wrapperToken": rpc_res.readString(),
        "expansionToken": rpc_res.readString(),
        "message": rpc_res.readString()
    }

    plot_extension_db = database_handler.find_item_by_token(plot_extension_details["expansionToken"])
    profile_handler.user.plotTopLeftX = plot_extension_details["plotTopLeftX"]
    profile_handler.user.plotTopLeftY = plot_extension_details["plotTopLeftY"]
    profile_handler.user.plotBottomRightX = plot_extension_details["plotBottomRightX"]
    profile_handler.user.plotBottomRightY = plot_extension_details["plotBottomRightY"]

    profile_handler.user.credits -= int(plot_extension_db["cost"])

    rpc_req.writeUintvar31(Events.PLOT_EXTENSION_SUCCESS)
    rpc_req.writeIntvar32(int(plot_extension_db["cost"]) * -1)

    return response.getvalue()
