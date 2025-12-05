from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Dict, Mapping

from .base import Datatype

if TYPE_CHECKING:  # pragma: no cover - used for static analysis only
    from ..datastream.input_data_stream import InputDataStream
    from ..datastream.output_data_stream import OutputDataStream


class BooleanDatatype(Datatype):
    def read(self, stream: "InputDataStream") -> bool:
        return stream.readBoolean()

    def write(self, stream: "OutputDataStream", value: Any) -> None:
        stream.writeBoolean(bool(value))


class StringDatatype(Datatype):
    def read(self, stream: "InputDataStream") -> str:
        return stream.readString()

    def write(self, stream: "OutputDataStream", value: Any) -> None:
        if value is None:
            raise ValueError(
                "Value is Null. Use Datatypes.NULLABLE_STRING to allow write null String values"
            )
        stream.writeString(str(value))


class Uint31Datatype(Datatype):
    def read(self, stream: "InputDataStream") -> int:
        return stream.readUintvar31()

    def write(self, stream: "OutputDataStream", value: Any) -> None:
        stream.writeUintvar31(int(value))


class NullableDatatype(Datatype):
    def __init__(self, datatype: Datatype) -> None:
        self._datatype = datatype

    def read(self, stream: "InputDataStream") -> Any:
        is_null = stream.readBoolean()
        if is_null:
            return None
        return self._datatype.read(stream)

    def write(self, stream: "OutputDataStream", value: Any) -> None:
        stream.writeBoolean(value is None)
        if value is not None:
            stream.writeValue(self._datatype, value)


@dataclass
class TypedData:
    type: Datatype
    value: Any

    def getValue(self) -> Any:
        return self.value

    def getType(self) -> Datatype:
        return self.type

    def __str__(self) -> str:  # pragma: no cover - debugging helper
        return f"Value : {self.getValue()}, type: {self.getType()}"


class MultiTypeMap:
    def __init__(self) -> None:
        self._map: Dict[int, TypedData] = {}

    def containsKey(self, key: int) -> bool:
        return int(key) in self._map

    def putUint31(self, key: int, value: int) -> None:
        self._map[int(key)] = TypedData(Datatypes.UINT31, int(value))

    def putString(self, key: int, value: str) -> None:
        if value is None:
            raise ValueError("Value is Null. This MultiTypeMap does not allow null String values")
        self._map[int(key)] = TypedData(Datatypes.STRING, str(value))

    def putBoolean(self, key: int, value: bool) -> None:
        self._map[int(key)] = TypedData(Datatypes.BOOLEAN, bool(value))

    def getUint31(self, key: int, default: int = 0) -> int:
        data = self._map.get(int(key))
        return default if data is None else int(data.getValue())

    def getString(self, key: int, default: str | None = None) -> str | None:
        data = self._map.get(int(key))
        if data is None or data.getValue() is None:
            return default
        return str(data.getValue())

    def getBoolean(self, key: int, default: bool = False) -> bool:
        data = self._map.get(int(key))
        return default if data is None else bool(data.getValue())

    def putUint31Map(self, mapping: Mapping[Any, Any]) -> None:
        for key, value in mapping.items():
            self._map[int(key)] = TypedData(Datatypes.UINT31, int(value))

    def putStringMap(self, mapping: Mapping[Any, Any]) -> None:
        for key, value in mapping.items():
            self._map[int(key)] = TypedData(Datatypes.STRING, value)

    def putBooleanMap(self, mapping: Mapping[Any, Any]) -> None:
        for key, value in mapping.items():
            self._map[int(key)] = TypedData(Datatypes.BOOLEAN, bool(value))

    def remove(self, key: int) -> bool:
        return self._map.pop(int(key), None) is not None

    def getSplitMultiTypeMap(self) -> "SplitMultiTypeMap":
        return SplitMultiTypeMap(self._map)

    def __str__(self) -> str:  # pragma: no cover - debugging helper
        lines = ["MultiTypeMap"]
        for key, data in self._map.items():
            lines.append(f" key: {key}, data: {data}")
        return "\n".join(lines)


class SplitMultiTypeMap:
    def __init__(self, mapping: Mapping[int, TypedData]) -> None:
        self._stringMap: Dict[str, Any] = {}
        self._uintMap: Dict[str, int] = {}
        self._booleanMap: Dict[str, bool] = {}
        for key, data in mapping.items():
            key_str = str(key)
            datatype = data.getType()
            if datatype is Datatypes.UINT31:
                self._uintMap[key_str] = int(data.getValue())
            elif datatype is Datatypes.BOOLEAN:
                self._booleanMap[key_str] = bool(data.getValue())
            elif datatype is Datatypes.STRING:
                self._stringMap[key_str] = data.getValue()

    def getUintMap(self) -> Dict[str, int]:
        return dict(self._uintMap)

    def getStringMap(self) -> Dict[str, Any]:
        return dict(self._stringMap)

    def getBooleanMap(self) -> Dict[str, bool]:
        return dict(self._booleanMap)


class MapDatatype(Datatype):
    UINT31_UINT31_MAP: "MapDatatype"
    UINT31_STRING_MAP: "MapDatatype"
    UINT31_BOOLEAN_MAP: "MapDatatype"

    def __init__(self, keyDatatype: Datatype, valueDatatype: Datatype) -> None:
        self._keyDatatype = keyDatatype
        self._valueDatatype = valueDatatype

    def read(self, stream: "InputDataStream") -> Dict[str, Any]:
        length = stream.readUintvar31()
        result: Dict[str, Any] = {}
        for _ in range(length):
            key = stream.readValue(self._keyDatatype)
            value = stream.readValue(self._valueDatatype)
            result[str(key)] = value
        return result

    def write(self, stream: "OutputDataStream", value: Mapping[Any, Any]) -> None:
        length = self._getMapSize(value)
        stream.writeUintvar31(length)
        for key, item in value.items():
            stream.writeValue(self._keyDatatype, key)
            stream.writeValue(self._valueDatatype, item)

    @staticmethod
    def _getMapSize(mapping: Mapping[Any, Any]) -> int:
        return sum(1 for _ in mapping.keys())


class MultiTypeMapDatatype(Datatype):
    RPC_DATATYPE: Datatype

    def read(self, stream: "InputDataStream") -> MultiTypeMap:
        uint_map = stream.readValue(MapDatatype.UINT31_UINT31_MAP)
        bool_map = stream.readValue(MapDatatype.UINT31_BOOLEAN_MAP)
        string_map = stream.readValue(MapDatatype.UINT31_STRING_MAP)
        result = MultiTypeMap()
        result.putUint31Map(uint_map)
        result.putBooleanMap(bool_map)
        result.putStringMap(string_map)
        return result

    def write(self, stream: "OutputDataStream", value: MultiTypeMap) -> None:
        split = value.getSplitMultiTypeMap()
        stream.writeValue(MapDatatype.UINT31_UINT31_MAP, split.getUintMap())
        stream.writeValue(MapDatatype.UINT31_BOOLEAN_MAP, split.getBooleanMap())
        stream.writeValue(MapDatatype.UINT31_STRING_MAP, split.getStringMap())


class Datatypes:
    UINT31: Datatype
    BOOLEAN: Datatype
    STRING: Datatype
    NULLABLE_STRING: Datatype


# Static initialisation mirroring the AS3 constants
Datatypes.UINT31 = Uint31Datatype()
Datatypes.BOOLEAN = BooleanDatatype()
Datatypes.STRING = StringDatatype()
Datatypes.NULLABLE_STRING = NullableDatatype(StringDatatype())

MapDatatype.UINT31_UINT31_MAP = MapDatatype(Datatypes.UINT31, Datatypes.UINT31)
MapDatatype.UINT31_STRING_MAP = MapDatatype(Datatypes.UINT31, Datatypes.STRING)
MapDatatype.UINT31_BOOLEAN_MAP = MapDatatype(Datatypes.UINT31, Datatypes.BOOLEAN)

MultiTypeMapDatatype.RPC_DATATYPE = NullableDatatype(MultiTypeMapDatatype())
