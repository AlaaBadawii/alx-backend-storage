#!/usr/bin/env python3
""" exercise module
"""
import redis
import uuid
from typing import Any, Union


class Cache():
    """ caching system
    """
    def __init__(self) -> None:
        """ Initials a cache instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ used to store data in the cache.
        """
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key
