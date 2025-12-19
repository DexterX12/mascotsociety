from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ...constants import Events
from ... import database_handler, profile_handler
from datetime import datetime, timezone

def handle_claim_completion_reward(stream:InputDataStream) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    reward = {
        "rewardId": rpc_res.readUintvar32(),
        "rewardType": rpc_res.readString()
    }

    reward_item = profile_handler.create_item({
        "itemHash": database_handler.completion_rewards[reward["rewardId"]],
        "createTime": datetime.now(timezone.utc)
    })

    profile_handler.user.completedSets.append(reward["rewardId"])

    rpc_req.writeUintvar31(Events.COMPLETION_SUCCESS)
    rpc_req.writeOwnedItem(reward_item)

    return response.getvalue()
