#!/usr/bin/env python3
""" exercise module
"""
import redis
import uuid
from typing import Any, Union, Callable, Optional


class Cache():
    """ caching system
    """
    def __init__(self) -> None:
        """ Initials a cache instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ used to store data in the cache.
        """
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(
            self, key: str,
            fn: Optional[Callable[[bytes], Union[str, int]]] = None
            ) -> Union[str, bytes, int, float, None]:
        """ get data from cache
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """ return the cached str values
        """
        return self.get(key).decode('utf-8')

    def get_int(self, key: str) -> int:
        """ return the cached int values
        """
        return int(self.get(key).decode('utf-8'))
