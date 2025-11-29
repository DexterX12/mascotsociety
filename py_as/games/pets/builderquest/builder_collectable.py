from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class BuilderCollectable:
    name: str = ""
    id: int = 0
    count: int = 0
    xp: int = 0
    activityStatus: int = 0
    requestDate: Optional[datetime] = None
    canAsk: bool = True
    currentCount: int = 0

    def isCollectableCompleted(self) -> bool:
        return self.count <= self.currentCount

    def isCollectableFinished(self) -> bool:
        return self.activityStatus > 0
