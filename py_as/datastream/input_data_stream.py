from __future__ import annotations

import io
import struct
from datetime import datetime, timezone
from typing import Any, BinaryIO, Callable, Dict, List, Optional, Union

from ..datatypes.base import ReadableDatatype  # type: ignore[attr-defined]

ByteSource = Union[BinaryIO, bytes, bytearray, memoryview]


class InputDataStream:
    """Binary reader that mirrors the semantics of the ActionScript implementation."""

    def __init__(self, source: ByteSource) -> None:
        if isinstance(source, (bytes, bytearray, memoryview)):
            self._input: BinaryIO = io.BytesIO(bytes(source))
        elif hasattr(source, "read"):
            self._input = source  # type: ignore[assignment]
        else:
            raise TypeError("Unsupported source type for InputDataStream")

    # ------------------------------------------------------------------
    # Primitive readers

    def read_uint8(self) -> int:
        data = self._input.read(1)
        if len(data) != 1:
            raise EOFError("Unexpected end of stream while reading uint8")
        return data[0]

    def read_uintvar32(self) -> int:
        result = 0
        while True:
            byte = self.read_uint8()
            result = (result << 7) | (byte & 0x7F)
            if (byte & 0x80) == 0:
                return result & 0xFFFFFFFF

    def read_uintvar31(self) -> int:
        value = self.read_uintvar32()
        if value & 0x80000000:
            raise ValueError(f"Found value out of range: {value:#x}")
        return value

    def read_intvar32(self) -> int:
        encoded = self.read_uintvar32()
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

    def read_float32(self) -> float:
        data = self._input.read(4)
        if len(data) != 4:
            raise EOFError("Unexpected end of stream while reading float32")
        return struct.unpack(">f", data)[0]

    def read_float64(self) -> float:
        data = self._input.read(8)
        if len(data) != 8:
            raise EOFError("Unexpected end of stream while reading float64")
        return struct.unpack(">d", data)[0]

    def read_boolean(self) -> bool:
        value = self.read_uint8()
        if value == 0:
            return False
        if value == 1:
            return True
        raise ValueError(f"Invalid boolean value on stream: {value}")

    def read_string(self) -> str:
        remaining_chars = self.read_uintvar32()
        chars: List[str] = []
        while remaining_chars > 0:
            first = self.read_uint8()
            code_point: int
            prefix = first >> 4
            if prefix in (0, 1, 2, 3, 4, 5, 6, 7):
                code_point = first
            elif prefix in (12, 13):
                code_point = (first & 0x1F) << 6
                code_point |= self._read_utf8_extension()
            elif prefix == 14:
                code_point = (first & 0x0F) << 12
                code_point |= self._read_utf8_extension() << 6
                code_point |= self._read_utf8_extension()
            else:
                raise ValueError(
                    f"Malformed UTF-8: found char beginning with octet {first}"
                )
            chars.append(chr(code_point))
            remaining_chars -= 1
        return "".join(chars)

    def _read_utf8_extension(self) -> int:
        value = self.read_uint8()
        if (value & 0xC0) != 0x80:
            raise ValueError(
                f"Malformed UTF-8: found invalid extension octet {value}"
            )
        return value & 0x3F

    def read_byte_array(self) -> bytes:
        length = self.read_uintvar32()
        data = self._input.read(length)
        if len(data) != length:
            raise EOFError("Unexpected end of stream while reading byte array")
        return data

    def read_date(self) -> Optional[datetime]:
        seconds = self.read_uintvar32()
        if seconds == 0:
            return None
        return datetime.fromtimestamp(seconds, tz=timezone.utc)

    # ------------------------------------------------------------------
    # Composite helpers

    def read_array(self, reader: Callable[[], Any]) -> List[Any]:
        length = self.read_uintvar32()
        return [reader() for _ in range(length)]

    def read_sparse_array(self, reader: Callable[[], Any]) -> List[Any]:
        count = self.read_uintvar32()
        values: Dict[int, Any] = {}
        max_index = -1
        for _ in range(count):
            index = self.read_uintvar32()
            values[index] = reader()
            if index > max_index:
                max_index = index
        if max_index < 0:
            return []
        result = [None] * (max_index + 1)
        for index, value in values.items():
            result[index] = value
        return result

    def read_associative_array(self, reader: Callable[[], Any]) -> Dict[str, Any]:
        length = self.read_uintvar32()
        result: Dict[str, Any] = {}
        for _ in range(length):
            key = self.read_string()
            result[key] = reader()
        return result

    def read_value(self, datatype: ReadableDatatype) -> Any:
        return datatype.read(self)

    # Aliases preserving the ActionScript-friendly names
    readUint8 = read_uint8
    readUintvar32 = read_uintvar32
    readUintvar31 = read_uintvar31
    readIntvar32 = read_intvar32
    readFloat32 = read_float32
    readFloat64 = read_float64
    readBoolean = read_boolean
    readString = read_string
    readByteArray = read_byte_array
    readDate = read_date
    readArray = read_array
    readSparseArray = read_sparse_array
    readAssociativeArray = read_associative_array
    readValue = read_value
