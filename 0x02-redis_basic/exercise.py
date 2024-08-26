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


def call_history(method: Callable) -> Callable:
    '''Tracks the call details of a method in a Cache class.
    '''
    @wraps(method)
    def invoker(self, *args, **kwargs) -> Any:
        '''Returns the method's output after storing its inputs and output.
        '''
        in_key = '{}:inputs'.format(method.__qualname__)
        out_key = '{}:outputs'.format(method.__qualname__)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(in_key, str(args))
        output = method(self, *args, **kwargs)
        if isinstance(self._redis, redis.Redis):
            self._redis.rpush(out_key, output)
        return output
    return invoker


def replay(method: Callable) -> None:
    """ display the history of calls of a particular function.
    """
    if method is None or not hasattr(method, '__self__'):
        return
    redis_store = getattr(method.__self__, '_redis', None)
    if not isinstance(redis_store, redis.Redis()):
        return
    name = method.__qualname__
    in_key = '{}:inputs'.format(name)
    out_key = '{}:outputs'.format(name)
    call_count = 0
    if redis_store.exists(name):
        call_count = int(redis_store.get(name))
    print('{} was called {} times:'.format(name, call_count))
    inputs = redis_store.lrange(in_key, 0, -1)
    outputs = redis_store.lrange(out_key, 0, -1)
    for input, output in zip(inputs, outputs):
        print('{}(*{}) -> {}'.format(
            name,
            input.decode("utf-8"),
            output,
        ))


class Cache():
    """ caching system
    """
    def __init__(self) -> None:
        """ Initials a cache instance.
        """
        self._redis = redis.Redis()
        self._redis.flushdb(True)

    @count_calls
    @call_history
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
