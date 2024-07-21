from typing import Any
from functools import lru_cache, wraps
import time

class CacheManager:
    """
    데이터 캐싱을 관리하는 클래스

    이 클래스는 키-값 쌍으로 데이터를 저장하고, 각 데이터에 대한 만료 시간을 관리합니다.
    캐시된 데이터는 지정된 만료 시간이 지나면 무효화됩니다. (LRU 캐시를 사용)

    Attributes:
        expiration_time (int): 캐시 항목의 만료 시간(초)
        cache (dict): 캐시된 데이터를 저장하는 딕셔너리
    """
    def __init__(self, expiration_time: int):
        """
        CacheManager 인스턴스를 초기화

        Args:
            key (str): 데이터를 식별하는 고유 키
            data (Any): 저장할 데이터
        """
        self.expiration_time = expiration_time
        self.cache = {}

    def cache_data(self, key: str, data: Any) -> None:
        """
        주어진 키에 데이터를 캐시합니다.

        Args:
            key (str): 캐시할 데이터의 키
            data (Any): 캐시할 데이터
        """
        self.cache[key] = {
            'data': data,
            'timestamp': time.time()
        }

    @lru_cache(maxsize=None)
    def get_cached_data(self, key: str) -> Any:
        """
        주어진 키에 해당하는 캐시된 데이터를 반환합니다.

        이 메서드는 lru_cache 데코레이터를 사용하여 추가적인 메모리 최적화를 제공합니다.

        Args:
            key (str): 검색할 데이터의 키

        Returns:
            Any: 캐시된 데이터. 데이터가 없거나 만료된 경우 None을 반환
        """
        cached_item = self.cache.get(key)
        if cached_item and time.time() - cached_item['timestamp'] < self.expiration_time:
            return cached_item['data']
        return None
