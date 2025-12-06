from datetime import datetime, timezone

import profile
from ..utils.pets.types import AuditChange, AuditChangeBatch, RpcOwnedItem
from ..constants import Actions
from .. import profile_handler

def handle_audit(audit_batch:list[AuditChangeBatch]) -> None:
    for audit in audit_batch:
        for audit_changes in audit.auditChanges:
            handle_audit_action(audit_changes)


def handle_audit_action(audit:AuditChange) -> None:
    action:int = audit.action

    print(audit)    
    if audit.itemId < 0:
        audit.itemId *= -1

    if action == Actions.SPAWN_ITEM:
        item_pos = profile_handler.user.getItemIndexById(audit.newItemId)
        if item_pos != -1 and profile_handler.user.ownedItems[item_pos].itemHash == audit.itemHash: return # Already exists (probably)!

        newItem = RpcOwnedItem()

        newItem.itemId = audit.newItemId
        newItem.itemHash = 94802198
        newItem.active = audit.active
        newItem.roomIndex = audit.roomIndex
        newItem.positionX = audit.positionX
        newItem.positionY = audit.positionY
        newItem.positionZ = audit.positionZ
        newItem.containedAmount = audit.containedAmount
        newItem.containedType = audit.containedType
        newItem.containedItem = audit.containedItem
        newItem.createTime = audit.createTime
        newItem.message = audit.message
        newItem.sender = audit.sender
        newItem.roomIndex = audit.roomIndex

        profile_handler.user.ownedItems.append(newItem)

    if action == Actions.DELETE_ITEM:
        item_pos = profile_handler.user.getItemIndexById(audit.itemId)
        profile_handler.user.ownedItems.pop(item_pos)
    
    if action == Actions.CHANGE_ITEM:
        item_pos = profile_handler.user.getItemIndexById(audit.itemId)

        if item_pos == -1: return

        profile_handler.user.ownedItems[item_pos].active = audit.active
        profile_handler.user.ownedItems[item_pos].roomIndex = audit.roomIndex
        profile_handler.user.ownedItems[item_pos].positionX = audit.positionX
        profile_handler.user.ownedItems[item_pos].positionY = audit.positionY
        profile_handler.user.ownedItems[item_pos].positionZ = audit.positionZ
        # profile_handler.user.ownedItems[item_pos].containedAmount = audit.containedAmount
        profile_handler.user.ownedItems[item_pos].containedType = audit.containedType
        # profile_handler.user.ownedItems[item_pos].containedItem = audit.containedItem
        profile_handler.user.ownedItems[item_pos].createTime = audit.createTime
        profile_handler.user.ownedItems[item_pos].message = audit.message
        # profile_handler.user.ownedItems[item_pos].sender = audit.sender

        

    
