import io
import struct
from datetime import datetime, timezone
from typing import Any, BinaryIO, Callable, Mapping, Sequence, Union

from ..datatypes.base import WriteableDatatype

ByteSink = Union[BinaryIO, bytearray, io.BytesIO]


class OutputDataStream:
    """Binary writer that stays compatible with the ActionScript data format."""

    def __init__(self, sink: ByteSink | None = None) -> None:
        if sink is None:
            self._output: BinaryIO = io.BytesIO()
        elif isinstance(sink, bytearray):
            self._output = io.BytesIO(sink)
        elif isinstance(sink, io.BytesIO):
            self._output = sink
        elif hasattr(sink, "write"):
            self._output = sink
        else:
            raise TypeError("Unsupported sink type for OutputDataStream")

    def writeUint8(self, value: int) -> None:
        if not 0 <= value <= 0xFF:
            raise ValueError(f"uint8 out of range: {value}")
        self._output.write(bytes((value,)))

    def writeUintvar32(self, value: int) -> None:
        value &= 0xFFFFFFFF
        if value & 0xF0000000:
            shift = 28
        elif value & 0x0FE00000:
            shift = 21
        elif value & 0x001FC000:
            shift = 14
        elif value & 0x00003F80:
            shift = 7
        else:
            shift = 0
        while shift > 0:
            byte = ((value >> shift) & 0x7F) | 0x80
            self.writeUint8(byte)
            shift -= 7
        self.writeUint8(value & 0x7F)

    def writeUintvar31(self, value: int) -> None:
        if value & 0x80000000:
            raise ValueError(f"Value out of range: {value}")
        self.writeUintvar32(value)

    def writeIntvar32(self, value: int) -> None:
        if value < 0:
            encoded = (((~value) & 0xFFFFFFFF) << 1) | 1
        else:
            encoded = (value << 1) & 0xFFFFFFFE
        self.writeUintvar32(encoded & 0xFFFFFFFF)

    def writeFloat32(self, value: float) -> None:
        self._output.write(struct.pack(">f", value))

    def writeFloat64(self, value: float) -> None:
        self._output.write(struct.pack(">d", value))

    def writeBoolean(self, value: bool) -> None:
        self.writeUint8(1 if value else 0)

    def writeString(self, value: str) -> None:
        encoded = value.encode("utf-8")
        self.writeUintvar32(len(value))
        self._output.write(encoded)

    def writeByteArray(self, value: Union[bytes, bytearray, memoryview]) -> None:
        raw = bytes(value)
        self.writeUintvar32(len(raw))
        self._output.write(raw)

    def writeDate(self, value: datetime | None) -> None:
        if value is None:
            self.writeUintvar32(0)
            return
        if value.tzinfo is None:
            seconds = int(value.replace(tzinfo=timezone.utc).timestamp())
        else:
            seconds = int(value.astimezone(timezone.utc).timestamp())
        self.writeUintvar32(seconds)

    def writeArray(self, values: Sequence[Any], writer: Callable[[Any], None]) -> None:
        self.writeUintvar32(len(values))
        for item in values:
            writer(item)

    def writeSparseArray(self, values: Union[Sequence[Any], Mapping[int, Any]], writer: Callable[[Any], None]) -> None:
        if isinstance(values, Mapping):
            if values:
                max_index = max(int(key) for key in values.keys())
                length = max_index + 1
            else:
                length = 0
            self.writeUintvar32(length)
            for key, val in values.items():
                self.writeUintvar32(int(key))
                writer(val)
            return
        length = len(values)
        self.writeUintvar32(length)
        for index, val in enumerate(values):
            self.writeUintvar32(index)
            writer(val)

    def writeStringMap(self, mapping: Mapping[str, Any], writer: Callable[[Any], None]) -> None:
        count = len(mapping)
        self.writeUintvar32(count)
        for key, value in mapping.items():
            self.writeString(key)
            writer(value)

    def writeValue(self, datatype: WriteableDatatype, value: Any) -> None:
        datatype.write(self, value)

    def getvalue(self) -> bytes:
        if isinstance(self._output, io.BytesIO):
            return self._output.getvalue()
        raise TypeError("Underlying sink does not support getvalue()")
