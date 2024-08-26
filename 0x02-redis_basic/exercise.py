#!/usr/bin/env python3
""" exercise module
"""
import redis
import uuid
from typing import Any, Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    '''Tracks the number of calls made to a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Invokes the given method after incrementing its call counter.
        '''
        if isinstance(self._redis, redis.Redis):
            self._redis.incr(method.__qualname__)
        return method(self, *args, **kwargs)
    return invoker


class Cache():
    """ caching system
    """
    def __init__(self) -> None:
        """ Initials a cache instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ used to store data in the cache.
        """
        data_key = str(uuid.uuid4())
        self._redis.set(data_key, data)
        return data_key

    def get(self, key: str,
            fn=None) -> Union[str, bytes, int, float, None]:
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
