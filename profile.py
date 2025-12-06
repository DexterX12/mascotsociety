from pathlib import Path
from typing import Dict, List, Optional, Union

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