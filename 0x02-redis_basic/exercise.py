#!/usr/bin/env python3
"""
Redis module
"""
import sys
from functools import wraps
from typing import Union, Optional, Callable
from uuid import uuid4

import redis

UnionOfTypes = Union[str, bytes, int, float]


def count_calls(method: Callable) -> Callable:
    """
    Decorator to count how many times methods of the Cache class are called.
    :param method: The method to decorate.
    :return: The decorated method.
    """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wraps the method."""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    Decorator to store input parameters and outputs in Redis.
    :param method: The method to decorate.
    :return: The decorated method.
    """
    key = method.__qualname__
    input_key = f"{key}:inputs"
    output_key = f"{key}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Wraps the method."""
        self._redis.rpush(input_key, str(args))
        res = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(res))
        return res

    return wrapper


class Cache:
    """
    Cache redis class
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
        Generates a random key (e.g. using uuid),
        stores the input data in Redis using the
        random key and returns the key.
        :param data: The data to store.
        :return: The generated key.
        """
        key = str(uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> UnionOfTypes:
        """
        Converts the data back to the desired format.
        :param key: The key for the data.
        :param fn: Optional function to convert data.
        :return: The converted data.
        """
        if fn:
            return fn(self._redis.get(key))
        data = self._redis.get(key)
        return data

    def replay(self, method: Callable):
        """
        Displays the history of calls for a given method.
        :param method: The method to replay.
        """
        key = method.__qualname__
        inputs = self._redis.lrange(f"{key}:inputs", 0, -1)
 