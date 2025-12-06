import io
import struct
from datetime import datetime, timezone
from typing import Any, BinaryIO, Callable, Dict, List, Optional, Union

from ..datatypes.base import ReadableDatatype

ByteSource = Union[BinaryIO, bytes, bytearray, memoryview]


class InputDataStream:
    """Binary reader that mirrors the semantics of the ActionScript implementation."""

    def __init__(self, source: ByteSource) -> None:
        if isinstance(source, (bytes, bytearray, memoryview)):
            self._input: BinaryIO = io.BytesIO(bytes(source))
        elif hasattr(source, "read"):
            self._input = source
        else:
            raise TypeError("Unsupported source type for InputDataStream")

    def readUint8(self) -> int:
        data = self._input.read(1)
        if len(data) != 1:
            raise EOFError("Unexpected end of stream while reading uint8")
        return data[0]

    def readUintvar32(self) -> int:
        result = 0
        while True:
            byte = self.readUint8()
            result = (result << 7) | (byte & 0x7F)
            if (byte & 0x80) == 0:
                return result & 0xFFFFFFFF

    def readUintvar31(self) -> int:
        value = self.readUintvar32()
        if value & 0x80000000:
            raise ValueError(f"Found value out of range: {value:#x}")
        return value

    def readIntvar32(self) -> int:
        encoded = self.readUintvar32()
        if encoded & 1:
            raw = encoded >> 1
            value = (~raw) & 0xFFFFFFFF
            if value & 0x80000000:
                value -= 0x100000000
            return value
        raw = (encoded >> 1) & 0x7FFFFFFF
        if raw & 0x40000000:
            raw -= 0x80000000
        return raw

    def readFloat32(self) -> float:
        data = self._input.read(4)
        if len(data) != 4:
            raise EOFError("Unexpected end of stream while reading float32")
        return struct.unpack(">f", data)[0]

    def readFloat64(self) -> float:
        data = self._input.read(8)
        if len(data) != 8:
            raise EOFError("Unexpected end of stream while reading float64")
        return struct.unpack(">d", data)[0]

    def readBoolean(self) -> bool:
        value = self.readUint8()
        if value == 0:
            return False
        if value == 1:
            return True
        raise ValueError(f"Invalid boolean value on stream: {value}")

    def readString(self) -> str:
        remaining_chars = self.readUintvar32()
        chars: List[str] = []
        while remaining_chars > 0:
            first = self.readUint8()
            code_point: int
            prefix = first >> 4
            if prefix in (0, 1, 2, 3, 4, 5, 6, 7):
                code_point = first
            elif prefix in (12, 13):
                code_point = (first & 0x1F) << 6
                code_point |= self._readUtf8Extension()
            elif prefix == 14:
                code_point = (first & 0x0F) << 12
                code_point |= self._readUtf8Extension() << 6
                code_point |= self._readUtf8Extension()
            else:
                raise ValueError(
                    f"Malformed UTF-8: found char beginning with octet {first}"
                )
            chars.append(chr(code_point))
            remaining_chars -= 1
        return "".join(chars)

    def _readUtf8Extension(self) -> int:
        value = self.readUint8()
        if (value & 0xC0) != 0x80:
            raise ValueError(
                f"Malformed UTF-8: found invalid extension octet {value}"
            )
        return value & 0x3F

    def readByteArray(self) -> bytes:
        length = self.readUintvar32()
        data = self._input.read(length)
        if len(data) != length:
            raise EOFError("Unexpected end of stream while reading byte array")
        return data

    def readDate(self) -> Optional[datetime]:
        seconds = self.readUintvar32()
        if seconds == 0:
            return None
        return datetime.fromtimestamp(seconds, tz=timezone.utc)

    def readArray(self, reader: Callable[[], Any]) -> List[Any]:
        length = self.readUintvar32()
        return [reader() for _ in range(length)]

    def readSparseArray(self, reader: Callable[[], Any]) -> List[Any]:
        count = self.readUintvar32()
        values: Dict[int, Any] = {}
        max_index = -1
        for _ in range(count):
            index = self.readUintvar32()
            values[index] = reader()
            if index > max_index:
                max_index = index
        if max_index < 0:
            return []
        result = [None] * (max_index + 1)
        for index, value in values.items():
            result[index] = value
        return result

    def readAssociativeArray(self, reader: Callable[[], Any]) -> Dict[str, Any]:
        length = self.readUintvar32()
        result: Dict[str, Any] = {}
        for _ in range(length):
            key = self.readString()
            result[key] = reader()
        return result

    def readValue(self, datatype: ReadableDatatype) -> Any:
        return datatype.read(self)
