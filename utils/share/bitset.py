from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Optional


class BitSet:
    """Simple bitset compatible with the ActionScript implementation."""

    def __init__(self) -> None:
        self._bits = bytearray()

    def get(self, index: int) -> bool:
        byte_index = index // 8
        bit_offset = 7 - index % 8
        if byte_index >= len(self._bits):
            return False
        return bool((self._bits[byte_index] >> bit_offset) & 1)

    def isEmpty(self) -> bool:
        return len(self._bits) == 0

    def cardinality(self) -> int:
        count = 0
        total_bits = len(self._bits) * 8
        for idx in range(total_bits):
            if self.get(idx):
                count += 1
        return count

    def length(self) -> int:
        last_bit = len(self._bits) * 8 - 1
        while last_bit >= 0:
            if self.get(last_bit):
                return last_bit + 1
            last_bit -= 1
        return 0

    def set(self, start: int, end: int = 0, value: bool = True) -> None:
        if end == 0:
            self._set(start, value)
            return
        for idx in range(start, end):
            self._set(idx, value)

    def clear(self, start: int = 0, end: int = 0) -> None:
        if start == 0 and end == 0:
            self._bits = bytearray()
            return
        if end == 0:
            self._set(start, False)
            return
        for idx in range(start, end):
            self._set(idx, False)

    def clone(self) -> "BitSet":
        clone = BitSet()
        clone._bits.extend(self._bits)
        return clone

    def setArray(self, data: bytes | bytearray) -> None:
        self._bits = bytearray(data)

    def getBitString(self) -> str:
        bits = []
        for byte in self._bits:
            bits.append(
                "".join(str((byte >> shift) & 1) for shift in range(7, -1, -1))
            )
        return "".join(bits)

    def __str__(self) -> str:
        return f"[bits={self.getBitString()}]"

    @property
    def bits(self) -> bytes:
        return bytes(self._bits)

    def _set(self, index: int, value: bool) -> None:
        byte_index = index // 8
        bit_offset = 7 - index % 8
        if byte_index >= len(self._bits):
            if not value:
                return
            self._grow(byte_index)
        if value:
            self._bits[byte_index] |= 1 << bit_offset
        else:
            self._bits[byte_index] &= ~(1 << bit_offset)

    def _grow(self, target_index: int) -> None:
        missing = target_index - len(self._bits)
        if missing > 0:
            self._bits.extend(b"\x00" * missing)
        self._bits.append(0)
