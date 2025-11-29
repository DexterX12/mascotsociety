from __future__ import annotations

import io
import struct
from datetime import datetime, timezone
from typing import Any, BinaryIO, Callable, Mapping, Sequence, Union

from ..datatypes.base import WriteableDatatype  # type: ignore[attr-defined]

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
            self._output = sink  # type: ignore[assignment]
        else:
            raise TypeError("Unsupported sink type for OutputDataStream")

    # ------------------------------------------------------------------
    # Primitive writers

    def write_uint8(self, value: int) -> None:
        if not 0 <= value <= 0xFF:
            raise ValueError(f"uint8 out of range: {value}")
        self._output.write(bytes((value,)))

    def write_uintvar32(self, value: int) -> None:
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
            self.write_uint8(byte)
            shift -= 7
        self.write_uint8(value & 0x7F)

    def write_uintvar31(self, value: int) -> None:
        if value & 0x80000000:
            raise ValueError(f"Value out of range: {value}")
        self.write_uintvar32(value)

    def write_intvar32(self, value: int) -> None:
        if value < 0:
            encoded = (((~value) & 0xFFFFFFFF) << 1) | 1
        else:
            encoded = (value << 1) & 0xFFFFFFFE
        self.write_uintvar32(encoded & 0xFFFFFFFF)

    def write_float32(self, value: float) -> None:
        self._output.write(struct.pack(">f", value))

    def write_float64(self, value: float) -> None:
        self._output.write(struct.pack(">d", value))

    def write_boolean(self, value: bool) -> None:
        self.write_uint8(1 if value else 0)

    def write_string(self, value: str) -> None:
        encoded = value.encode("utf-8")
        self.write_uintvar32(len(value))
        self._output.write(encoded)

    def write_byte_array(self, value: Union[bytes, bytearray, memoryview]) -> None:
        raw = bytes(value)
        self.write_uintvar32(len(raw))
        self._output.write(raw)

    def write_date(self, value: datetime | None) -> None:
        if value is None:
            self.write_uintvar32(0)
            return
        if value.tzinfo is None:
            seconds = int(value.replace(tzinfo=timezone.utc).timestamp())
        else:
            seconds = int(value.astimezone(timezone.utc).timestamp())
        self.write_uintvar32(seconds)

    # ------------------------------------------------------------------
    # Composite helpers

    def write_array(self, values: Sequence[Any], writer: Callable[[Any], None]) -> None:
        self.write_uintvar32(len(values))
        for item in values:
            writer(item)

    def write_sparse_array(self, values: Union[Sequence[Any], Mapping[int, Any]], writer: Callable[[Any], None]) -> None:
        if isinstance(values, Mapping):
            if values:
                max_index = max(int(key) for key in values.keys())
                length = max_index + 1
            else:
                length = 0
            self.write_uintvar32(length)
            for key, val in values.items():
                self.write_uintvar32(int(key))
                writer(val)
            return
        length = len(values)
        self.write_uintvar32(length)
        for index, val in enumerate(values):
            self.write_uintvar32(index)
            writer(val)

    def write_string_map(self, mapping: Mapping[str, Any], writer: Callable[[Any], None]) -> None:
        count = len(mapping)
        self.write_uintvar32(count)
        for key, value in mapping.items():
            self.write_string(key)
            writer(value)

    def write_value(self, datatype: WriteableDatatype, value: Any) -> None:
        datatype.write(self, value)

    # ------------------------------------------------------------------

    def getvalue(self) -> bytes:
        if isinstance(self._output, io.BytesIO):
            return self._output.getvalue()
        raise TypeError("Underlying sink does not support getvalue()")

    # Aliases preserving the ActionScript-friendly names
    writeUint8 = write_uint8
    writeUintvar32 = write_uintvar32
    writeUintvar31 = write_uintvar31
    writeIntvar32 = write_intvar32
    writeFloat32 = write_float32
    writeFloat64 = write_float64
    writeBoolean = write_boolean
    writeString = write_string
    writeByteArray = write_byte_array
    writeDate = write_date
    writeArray = write_array
    writeSparseArray = write_sparse_array
    writeStringMap = write_string_map
    writeValue = write_value
