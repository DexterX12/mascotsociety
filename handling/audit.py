from ..utils.pets.types import AuditChange, AuditChangeBatch, RpcOwnedItem
from ..constants import Actions
from .. import profile_handler
from .. import database_handler
from ..utils.hash import hashInt32

def handle_audit(audit_batch:list[AuditChangeBatch]) -> None:
    for audit in audit_batch:
        for audit_changes in audit.auditChanges:
            handle_audit_action(audit_changes)

def set_item_data(new_item:RpcOwnedItem, audit: AuditChange):
    new_item.active = audit.active
    new_item.containedType = audit.containedType
    new_item.createTime = audit.createTime
    new_item.message = audit.message
    new_item.positionX = audit.positionX
    new_item.positionY = audit.positionY
    new_item.positionZ = audit.positionZ
    new_item.roomIndex = audit.roomIndex


def handle_audit_action(audit:AuditChange) -> None:
    action:int = audit.action

    if audit.itemId < 0:
        audit.itemId *= -1

    if audit.newItemId < 0:
        audit.newItemId *= -1

    print(audit)

    if (action == Actions.SPAWN_ITEM or
        action == Actions.BUY_ITEM_COINS):
                    
        item_db = database_handler.findItemByToken(audit.token)

        new_item = RpcOwnedItem()
        new_item.itemId = audit.newItemId

        # THIS NEEDS TO BE HASHED THE SAME WAY AS THE CLIENT ACTIONSCRIPT HASH
        new_item.itemHash = hashInt32(item_db["name"])

        set_item_data(new_item, audit)

        profile_handler.user.ownedItems.append(new_item)

    if action == Actions.DELETE_ITEM:
        item_pos = profile_handler.user.getItemIndexById(audit.itemId)

        if item_pos == -1:
            print("Item not found with id = ", audit.itemId)
            return

        print("Deleting item with ID =", audit.itemId, "and hash =", profile_handler.user.ownedItems[item_pos].itemHash)
        
        profile_handler.user.ownedItems.pop(item_pos)

    
    if action == Actions.SELL_ITEM:
        item_pos = profile_handler.user.getItemIndexById(audit.itemId)

        if item_pos == -1:
            print("Item not found with id = ", audit.itemId)
            return

        print("Selling item with ID =", audit.itemId, "and hash =", profile_handler.user.ownedItems[item_pos].itemHash)
        
        profile_handler.user.ownedItems.pop(item_pos)
        profile_handler.user.credits = audit.newCredits

    
    if action == Actions.CHANGE_ITEM:
        item_pos = profile_handler.user.getItemIndexById(audit.itemId)
        if item_pos == -1: return

        updated_item = profile_handler.user.ownedItems[item_pos]

        set_item_data(updated_item, audit)
    
    if action == Actions.OPEN_ITEM:

        item_pos = profile_handler.user.getItemIndexById(audit.itemId)
        if item_pos == -1: return

        new_item = RpcOwnedItem()
        new_item.itemId = audit.newItemId
        new_item.itemHash = audit.itemHash

        set_item_data(new_item, audit)

        profile_handler.user.ownedItems.append(new_item)
        profile_handler.user.ownedItems.pop(item_pos)

        

    
