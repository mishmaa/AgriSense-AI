from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Any


@dataclass
class CacheEntry:
    value: Any
    expires_at: float


class TTLCache:
    def __init__(self) -> None:
        self._store: dict[str, CacheEntry] = {}

    def get(self, key: str) -> Any | None:
        entry = self._store.get(key)
        if not entry:
            return None
        if entry.expires_at < time.time():
            self._store.pop(key, None)
            return None
        return entry.value

    def set(self, key: str, value: Any, ttl_seconds: int = 30) -> Any:
        self._store[key] = CacheEntry(value=value, expires_at=time.time() + ttl_seconds)
        return value

    def invalidate_prefix(self, prefix: str) -> None:
        for key in list(self._store):
            if key.startswith(prefix):
                self._store.pop(key, None)


app_cache = TTLCache()
