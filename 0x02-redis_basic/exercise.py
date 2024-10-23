#!/usr/bin/env python3
"""
Redis module for caching functionality.
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
    
    :param method: The method to wrap.
    :return: The wrapped method with call counting.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Increments the call count in Redis for the method.

        :param self: The instance of the class.
        :param args: Positional arguments for the method.
        :param kwargs: Keyword arguments for the method.
        :return: The result of the original method.
        """
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper

def call_history(method: Callable) -> Callable:
    """
    Decorator to record the input parameters and output
    of a method in Redis.

    :param method: The method to wrap.
    :return: The wrapped method with call history.
    """
    key = method.__qualname__
    input_key = f"{key}:inputs"
    output_key = f"{key}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Records input and output for the method.

        :param self: The instance of the class.
        :param args: Positional arguments for the method.
        :param kwargs: Keyword arguments for the method.
        :return: The result of the original method.
        """
        self._redis.rpush(input_key, str(args))
        result = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(result))
        return result

    return wrapper

class Cache:
    """
    Cache class for managing Redis operations.
    """

    def __init__(self):
        """
        Initializes the Cache instance and flushes the Redis database.
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: UnionOfTypes) -> str:
        """
        Stores input data in Redis with a randomly generated key.

        :param data: The data to store (can be str, bytes, int, or float).
        :return: The key under which the data is stored.
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> UnionOfTypes:
        """
        Retrieves data from Redis and converts it using a provided function.

        :param key: The key of the data to retrieve.
        :param fn: An optional function to convert the data.
        :return: The retrieved (and possibly converted) data.
        """
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_int(self: bytes) -> int:
        """Converts bytes to an integer."""
        return int.from_bytes(self, sys.byteorder)

    def get_str(self: bytes) -> str:
        """Converts bytes to a string."""
        return self.decode("utf-8")
