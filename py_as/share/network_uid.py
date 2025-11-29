from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NetworkUid:
    _network: int
    _networkUid: str
    _playfishUid: int

    FACEBOOK: int = 2
    MYSPACE: int = 3
    BEBO: int = 4
    YAHOO: int = 5
    NETLOG: int = 6
    IGOOGLE: int = 7
    INTERNAL_USER: int = 0xFFFFFFFF

    @staticmethod
    def areEqual(left: "NetworkUid", right: "NetworkUid") -> bool:
        return left._network == right._network and left._networkUid == right._networkUid

    @staticmethod
    def create(network: int, network_uid: str) -> "NetworkUid":
        return NetworkUid(network, network_uid, 0)

    @property
    def network(self) -> int:
        return self._network

    @property
    def networkUid(self) -> str:
        return self._networkUid

    @property
    def playfishUid(self) -> int:
        return self._playfishUid

    @property
    def seed(self) -> int:
        seed_value = 1480002569 + self._network * 3571
        for char in self._networkUid:
            seed_value = seed_value * 23 + ord(char)
        return seed_value & 0xFFFFFFFF

    def __str__(self) -> str:  # pragma: no cover - debugging helper
        return f"{self._network}:{self._networkUid}"

