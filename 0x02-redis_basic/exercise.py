#!/usr/bin/env python3
"""
Redis module for caching data.
"""
import sys
from functools import wraps
from typing import Union, Optional, Callable
from uuid import uuid4

import redis

UnionOfTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times a method is called.
    :param method: The method to decorate.
    :return: The wrapped method.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Increments call count in Redis."""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to log input and output in Redis.
    :param method: The method to decorate.
    :return: The wrapped method.
    """
    key = method.__qualname__
    input_key = f"{key}:inputs"
    output_key = f"{key}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Stores inputs and outputs in Redis."""
        self._redis.rpush(input_key, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(res))
        return res

    return wrapper


class Cache:
    """
    Cache class to interface with Redis.
    """

    def __init__(self):
        """
        Initializes the cache and clears the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: UnionOfTypes) -> str:
        """
        Stores data in Redis with a unique key.
        :param data: The data to store.
        :return: The generated key.
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> UnionOfTypes:
        """
        Retrieves data from Redis and optionally converts it.
        :param key: The key for the data.
        :param fn: Optional conversion function.
        :return: The retrieved (and possibly converted) data.
        """
        if fn:
            return fn(self._redis.get(key))
        data = self._redis.get(key)
        return data

    def replay(self, method: Callable):
        """
        Shows the history of calls for a specific method.
        :param method: The method to replay.
        """
        key = method.__qualname__
        inputs = self._redis.lrange(f"{key}:inputs", 0, -1)
        