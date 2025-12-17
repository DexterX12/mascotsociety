from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from .utils.pets.rpc_request import RpcRequest
from .utils.datastream.output_data_stream import OutputDataStream
from .utils.datastream.input_data_stream import InputDataStream
from .utils.pets.rpc_response import RpcResponse
from .utils.pets.user_info import UserInfo
from .utils.pets.types import RpcOwnedItem

class Profile:
    def __init__(self) -> None:
        self.cash: int = 0
        self.new_house_data: Optional[Dict[str, int]] = None
        self.user: Optional[UserInfo] = None
        self.friends: List[UserInfo] = []
        self.loaded_file: Optional[Path] = None

        # if the client wants to create a duplicated ID, just map it to a new item
        self.duplicate_cache: dict[int, int] = {}

    def load_from_file(self, file_path: Union[str, Path, bytes, bytearray]) -> None:

        if isinstance(file_path, (bytes, bytearray)):
            data = bytes(file_path)
            self.loaded_file = None
        else:
            path = Path(file_path)
            data = path.read_bytes()
            self.loaded_file = path

        response = RpcResponse(InputDataStream(data))
        self.cash = response.readUintvar31()
        self.new_house_data = response.readNewHouseData()
        self.user = response.readUserInfo()
        try:
            self.friends = response.readArray(response.readUserInfo)
        except (EOFError, ValueError):
            self.friends = []

    
    def detect_duplicates(self) -> None:
        if not self.user or not self.user.ownedItems:
            return

        max_item_id = max(item.itemId for item in self.user.ownedItems)
        seen_ids = set()

        for item in self.user.ownedItems:
            item_id = item.itemId

            if item_id not in seen_ids:
                seen_ids.add(item_id)
                continue

            max_item_id += 1
            while max_item_id in seen_ids:
                max_item_id += 1

            item.itemId = max_item_id
            seen_ids.add(max_item_id)

    def _getItemIndexById(self, itemId:int) -> int:
        for i in range(len(self.user.ownedItems)):
            if not self.user.ownedItems[i].itemId == itemId: continue
            return i
        return -1
    
    def _getItemIndexByHash(self, itemHash:int) -> int:
        for i in range(len(self.user.ownedItems)):
            if not self.user.ownedItems[i].itemHash == itemHash: continue
            return i
        return -1
    
    def _scoreItemsByProperties(self, item1:RpcOwnedItem, item2:RpcOwnedItem) -> int:
        score = 0

        if item1.itemHash and item2.itemHash and item1.itemHash == item2.itemHash:
            score += 24

        if item1.active == item2.active:
            score += 16

        if item1.roomIndex == item2.roomIndex:
            score += 10
        else:
            score -= 5

        # On most (and currently seen) cases, the item's position gives a lot
        # of clues if the item to change is the correct one
        if item1.positionX == item2.positionX:
            score += 12
        else:
            score -= 24

        if item1.positionY == item2.positionY:
            score += 12
        else:
            score -= 24

        if item1.positionZ == item2.positionZ:
            score += 12
        else:
            score -= 24

        if item1.containedType == item2.containedType:
            score += 2

        return score
    
    def _mapItem(self, item:RpcOwnedItem, data:dict[str, Any]) -> None:
        if "itemId" in data:
            item.itemId = data["itemId"]

        if "itemHash" in data and data["itemHash"] != 0:
            item.itemHash = data["itemHash"]
        
        if "active" in data:
            item.active = data["active"]
        
        if "roomIndex" in data and data["roomIndex"] != 0:
            item.roomIndex = data["roomIndex"]
        
        if "positionX" in data and data["positionX"] != 0:
            item.positionX = data["positionX"]
        
        if "positionY" in data and data["positionY"] != 0:
            item.positionY = data["positionY"]
        
        if "positionZ" in data and data["positionZ"] != 0:
            item.positionZ = data["positionZ"]
        
        if "containedType" in data and data["containedType"] != 0:
            item.containedType = data["containedType"]
        
        if "containedType2" in data and data["containedType2"] != 0:
            item.containedItem2 = data["containedType2"]

        if "containedItem" in data and data["containedItem"] != 0:
            item.containedItem = data["containedItem"]
        
        if "containtedItem2" in data and data["containeditem2"] != 0:
            item.containedItem2 = data["containeditem2"]

        if "createTime" in data and data["createTime"] != None:
            item.createTime = data["createTime"]

        if "message" in data and data["message"] != "":
            item.message = data["message"]

        if "containedAmount" in data and data["containedAmount"] != 0:
            item.containedAmount = data["containedAmount"]

        if "sender" in data and data["message"] != None:
            item.sender = data["sender"]

    def _selectItemToMutate(self, itemAudit: RpcOwnedItem) -> int:
        if itemAudit.itemId in self.duplicate_cache.keys():
            item_dup_index = self._getItemIndexById(self.duplicate_cache[itemAudit.itemId])
            item_dup = self.user.ownedItems[item_dup_index]

            item_orig_index = self._getItemIndexById(itemAudit.itemId)
            item_orig = self.user.ownedItems[item_orig_index]

            item_orig_score = self._scoreItemsByProperties(item_orig, itemAudit)
            item_dup_score = self._scoreItemsByProperties(item_dup, itemAudit)

            if item_orig_score > item_dup_score: return item_orig_index
            else: return item_dup_index
        else:
            itemId = self._getItemIndexById(itemAudit.itemId)

            if itemId != -1:
                return itemId

            # what if no itemId is provided? (delete by Hash)
            return self._getItemIndexByHash(itemAudit.itemHash)

    
    def create_item(self, data:dict[str, Any]) -> RpcOwnedItem:
        new_item = RpcOwnedItem()
        max_id = max(item.itemId for item in self.user.ownedItems)

        self._mapItem(new_item, data)

        if "itemId" in data:
            item_exists = self._getItemIndexById(data["itemId"]) != -1

            if item_exists:
                new_item_id = max_id + 1
                self.duplicate_cache[data["itemId"]] = new_item_id
                new_item.itemId = new_item_id
        else:
            new_item.itemId = max_id + 1
        
        self.user.ownedItems.append(new_item)

        return new_item

    def delete_item(self, data:dict[str, Any]) -> RpcOwnedItem:
        item = RpcOwnedItem()
        self._mapItem(item, data)

        item_index = self._selectItemToMutate(item)

        if item_index != self._getItemIndexById(item.itemId) and item.itemId != -1:
            del self.duplicate_cache[item.itemId]

        return self.user.ownedItems.pop(item_index)
        
    def update_item(self, data:dict[str, Any]) -> None:
        item = RpcOwnedItem()
        self._mapItem(item, data)
        item_index = 0

        # This assumes duplicate ID data do not come
        # from updating outside of audits, only creating
        #
        # This is important due to not having to re-fill
        # existing items manually

        if "audit" in data and data["audit"] == False: 
            item_index = self._getItemIndexById(data["itemId"])
        else:
            item_index = self._selectItemToMutate(item)

        item = self.user.ownedItems[item_index]
        self._mapItem(item, data)
        

    def save_file(self) -> None:
        if self.user is None or self.loaded_file is None:
            raise ValueError("Profile data is not loaded; cannot save.")

        new_house_data = self.new_house_data if self.new_house_data is not None else {}

        user_data = RpcRequest(OutputDataStream())
        user_data.writeUintvar31(self.cash)
        user_data.writeNewHouseData(new_house_data)
        user_data.writeUserInfo(self.user)
        user_data.writeArray(self.friends, user_data.writeUserInfo)

        self.loaded_file.write_bytes(user_data.getvalue())
