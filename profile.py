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
