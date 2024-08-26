#!/usr/bin/env python3
""" exercise module
"""
import redis
import uuid
from typing import Any


class Cache():
    """ caching system
    """
    def __init__(self) -> None:
        """ Initials a cache instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Any) -> str:
        """ used to store data in the cache.
        """
        key = str(uuid.uuid4())

        if isinstance(data, (int, float)):
            value = str(data)
        elif isinstance(data, bytes):
            value = data.decode('utf-8')
        elif isinstance(data, str):
            value = data
        else:
            raise TypeError("Unsupported data type")

        self._redis.set(key, value)
        return key
