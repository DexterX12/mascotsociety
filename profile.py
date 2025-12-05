from pathlib import Path
from typing import Dict, List, Optional, Union

from utils.datastream.input_data_stream import InputDataStream
from utils.pets.rpc_response import RpcResponse
from utils.pets.types import RpcOwnedItem
from utils.pets.user_info import UserInfo
from utils.share.network_uid import NetworkUid


class ProfileHandler:

    def __init__(self) -> None:
        self.cash: int = 0
        self.new_house_data: Optional[Dict[str, int]] = None
        self.user: Optional[UserInfo] = None
        self.friends: List[UserInfo] = []
        self.loaded_file: Optional[Path] = None
        self.owned_items_cache: Dict[str, RpcOwnedItem] = {}
        self.max_id: int = 0
        self.save_number: int = 0

    def load_from_file(self, file_path: Union[str, Path, bytes, bytearray]) -> None:
        self.save_number = 0

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

        self._refresh_owned_items_cache()


    def _refresh_owned_items_cache(self) -> None:
        self.owned_items_cache = {}
        self.max_id = 0

        if not self.user or not self.user.ownedItems:
            return

        for item in self.user.ownedItems:
            if not isinstance(item, RpcOwnedItem):
                continue
            self.owned_items_cache[str(item.itemId)] = item
            if item.itemId > self.max_id:
                self.max_id = item.itemId
