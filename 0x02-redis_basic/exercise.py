#!/usr/bin/env python3
"""A program that allows python to interact with a redis database"""
import uuid
from typing import Callable
import redis


def call_history(func: Callable) -> Callable:
    """
    A function that store the history of inputs and outputs for a
    particular function.
    """
    def wrapper(*args, **kwargs):
        key_inputs = f"{func.__qualname__}:inputs"
        key_outputs = f"{func.__qualname__}:outputs"
        redis_instance = redis.Redis()
        inputs = str(args) + str(kwargs)
        output = func(*args, **kwargs)
        redis_instance.rpush(key_inputs, inputs)
        redis_instance.rpush(key_outputs, output)
        return output
    return wrapper


class Cache:
    def __init__(self):
        """
        A function that initializes a Redis instance and flushes it
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    def store(self, data: (str, bytes, int, float)) -> str:
        """
        A function that generates a random key using the uuid module
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None):
        """
        A function that retrieves the value stored in Redis
        """
        value = self._redis.get(key)
        if value is None:
            return None
        if fn is not None:
            return fn(value)
        return value

    def get_str(self, key: str) -> str:
        """Interacts with the get function"""
        return self.get(key, str)

    def get_int(self, key: str) -> int:
        """Interacts with the get function"""
        return self.get(key, int)

    def count_calls(self, func: Callable) -> Callable:
        """
        A function that increments the count for a given function
        key every time the function is called
        """
        def wrapper(*args, **kwargs):
            key = func.__qualname__
            count_key = f"{key}:count"
            redis_instance = redis.Redis()
            redis_instance.incr(count_key)
            return func(*args, **kwargs)
        return wrapper

    def replay(self, func: Callable):
        """
        A function that prints the input/output history for a given
        function key
        """
        key_inputs = f"{func.__qualname__}:inputs"
        key_outputs = f"{func.__qualname__}:outputs"
        redis_instance = redis.Redis()
        inputs = redis_instance.lrange(key_inputs, 0, -1)
        outputs = redis_instance.lrange(key_outputs, 0, -1)
        for input_, output in zip(inputs, outputs):
            print(f"{func.__name__}{input_} -> {output}")
