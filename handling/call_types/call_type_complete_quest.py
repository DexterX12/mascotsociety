from ...utils.datastream.output_data_stream import OutputDataStream
from ...utils.pets.rpc_request import RpcRequest
from ...utils.pets.rpc_response import InputDataStream, RpcResponse
from ...utils.pets.types import RpcQuestReward, RpcQuestTracker
from ...utils.hash import hashInt32
from ...constants import Events, ContainedTypes
from ...constants.mystery import Mystery
from ... import database_handler, profile_handler

from random import choice

def handle_complete_quest(stream:InputDataStream) -> bytes:
    response = OutputDataStream()
    rpc_res = RpcResponse(stream)
    rpc_req = RpcRequest(response)

    quest_max_steps = 5
    quest_xp = 20
    completed_quest = False
    current_step = 0

    quest_id = rpc_res.readUintvar31()
    user_quests = profile_handler.user.questTrackers
    step_reward = RpcQuestReward()
    step_reward.xp = quest_xp

    if len(user_quests) == 0:
        quest = RpcQuestTracker()
        quest.questId = quest_id
        quest.stepsCompleted, current_step = 1, 1
    else:
        for quest in user_quests:
            if quest.questId != quest_id: continue
            
            quest.stepsCompleted += 1
            current_step = quest.stepsCompleted

            if quest.stepsCompleted == quest_max_steps:
                completed_quest = True
                quest.stepsCompleted = 0
            

    rpc_req.writeUintvar31(Events.QUEST_COMPLETE_SUCCESS)
    rpc_req.writeUintvar31(current_step)
    rpc_req.writeQuestReward(step_reward)

    if completed_quest:
        complete_reward = RpcQuestReward()
        reward_item = database_handler.find_item_by_name("Mystery Box")
        contained_reward_name = choice(Mystery.MYSTERY_BOX)

        created_reward = profile_handler.create_item({
            "itemHash": reward_item["itemHash"],
            "containedType": ContainedTypes.CONTAINED_TREASURE,
            "containedItem": hashInt32(contained_reward_name)
        })

        complete_reward.itemId = created_reward.itemId
        complete_reward.itemHash = created_reward.itemHash
        complete_reward.containedType = created_reward.containedType
        complete_reward.containedItem = created_reward.containedItem

        rpc_req.writeQuestReward(complete_reward)
        print(complete_reward)
    else:
        rpc_req.writeQuestReward(RpcQuestReward())

    return response.getvalue()
