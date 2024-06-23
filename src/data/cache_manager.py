from typing import Any
from functools import lru_cache, wraps
import time

class CacheManager:
    def __init__(self, expiration_time: int):
        self.expiration_time = expiration_time
        self.cache = {}

    def cache_data(self, key: str, data: Any) -> None:
        self.cache[key] = {
            'data': data,
            'timestamp': time.time()
        }

    @lru_cache(maxsize=None)
    def get_cached_data(self, key: str) -> Any:
        cached_item = self.cache.get(key)
        if cached_item and time.time() - cached_item['timestamp'] < self.expiration_time:
            return cached_item['data']
        return None
