from ..utils.pets.types import AuditChange, AuditChangeBatch
from ..constants import Actions, Recipes
from .. import profile_handler
from .. import database_handler
from ..utils.hash import hashInt32

def handle_audit(audit_batch:list[AuditChangeBatch]) -> None:
    for audit in audit_batch:
        for audit_changes in audit.auditChanges:
            handle_audit_action(audit_changes)

def set_item_data(audit: AuditChange):
    item_data = {}

    item_data["active"] = audit.active
    item_data["containedType"] = audit.containedType
    item_data["createTime"] = audit.createTime
    item_data["message"] = audit.message
    item_data["positionX"] = audit.positionX
    item_data["positionY"] = audit.positionY
    item_data["positionZ"] = audit.positionZ
    item_data["roomIndex"] = audit.roomIndex

    return item_data


def handle_audit_action(audit:AuditChange) -> None:
    action:int = audit.action

    if audit.itemId < 0:
        audit.itemId *= -1

    if audit.newItemId < 0:
        audit.newItemId *= -1

    print(audit)

    if (action == Actions.SPAWN_ITEM or
        action == Actions.BUY_ITEM_COINS):
                    
        item_db = database_handler.find_item_by_token(audit.token)
        item_data = set_item_data(audit)
        item_data["itemId"] = audit.newItemId

        # The hashing has to be done the same way as the AS3 script does it
        item_data["itemHash"] = hashInt32(item_db["name"])

        profile_handler.create_item(item_data)

    if action == Actions.DELETE_ITEM:
        item_data = set_item_data(audit)
        item_data["itemId"] = audit.itemId

        profile_handler.delete_item(item_data)

        print("Deleting item with ID =", audit.itemId)

    if action == Actions.SELL_ITEM:
        item_data = set_item_data(audit)
        item_data["itemId"] = audit.itemId

        profile_handler.delete_item(item_data)

        print("Selling item with ID =", audit.itemId)

        profile_handler.user.credits = audit.newCredits

    
    if action == Actions.CHANGE_ITEM:
        item_data = set_item_data(audit)
        item_data["itemId"] = audit.itemId

        profile_handler.update_item(item_data)
    
    if action == Actions.OPEN_ITEM:
        item_data = set_item_data(audit)
        item_data["itemId"] = audit.newItemId
        item_data["itemHash"] = audit.itemHash

        profile_handler.create_item(item_data)

        profile_handler.delete_item({
            "itemId": audit.itemId
        })

    if action == Actions.FINISH_COOKING:
        item_data = set_item_data(audit)
        item_data["itemId"] = audit.newItemId
        item_data["itemHash"] = audit.itemHash

        profile_handler.create_item(item_data)

        profile_handler.update_item({
            "itemId": audit.itemId,
            "containedType": 0,
            "containedItem": 0,
            "createTime": None
        })

        # Since the game does not send delete actions
        # for some reason after cooking, manually delete
        # all cooking items from current recipe

        cooking_items = Recipes.MATERIALS_MAPPING[Recipes.HASHES.index(audit.itemHash)]

        for cooking_item_hash in cooking_items:
            profile_handler.delete_item({
                "itemId": -1,
                "itemHash": cooking_item_hash
            })
        

    
