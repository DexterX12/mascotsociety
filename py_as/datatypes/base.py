from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # pragma: no cover
    from ..datastream.input_data_stream import InputDataStream
    from ..datastream.output_data_stream import OutputDataStream


class ReadableDatatype(ABC):
    """Protocol for datatypes that know how to read themselves from a stream."""

    @abstractmethod
    def read(self, stream: "InputDataStream") -> Any:  # noqa: D401
        """Read a value from the provided data stream."""
        raise NotImplementedError


class WriteableDatatype(ABC):
    """Protocol for datatypes that know how to write themselves to a stream."""

    @abstractmethod
    def write(self, stream: "OutputDataStream", value: Any) -> None:  # noqa: D401
        """Write a value to the provided data stream."""
        raise NotImplementedError


class Datatype(ReadableDatatype, WriteableDatatype):
    """Combination of readable and writeable behaviours."""
