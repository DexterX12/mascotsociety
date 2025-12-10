from pathlib import Path
from typing import Dict, List, Optional, Union

from .utils.pets.rpc_request import RpcRequest
from .utils.datastream.output_data_stream import OutputDataStream
from .utils.datastream.input_data_stream import InputDataStream
from .utils.pets.rpc_response import RpcResponse
from .utils.pets.user_info import UserInfo

class Profile:
    def __init__(self) -> None:
        self.cash: int = 0
        self.new_house_data: Optional[Dict[str, int]] = None
        self.user: Optional[UserInfo] = None
        self.friends: List[UserInfo] = []
        self.loaded_file: Optional[Path] = None

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
        self._detect_duplicates()
        try:
            self.friends = response.readArray(response.readUserInfo)
        except (EOFError, ValueError):
            self.friends = []

    
    def _detect_duplicates(self) -> None:
        max_item_id = max(item.itemId for item in self.user.ownedItems)

        for item in self.user.ownedItems:
            for item_inner in self.user.ownedItems:
                if item == item_inner: continue
                if item.itemId != item_inner.itemId: continue

                item_inner.itemId = max_item_id + 1
                max_item_id += 1

    def save_file(self) -> None:
        user_data = RpcRequest(OutputDataStream())
        user_data.writeUintvar31(self.cash)
        user_data.writeNewHouseData(self.new_house_data)
        user_data.writeUserInfo(self.user)
        user_data.writeArray(self.friends, user_data.writeUserInfo)

        self.loaded_file.write_bytes(user_data.getvalue())
