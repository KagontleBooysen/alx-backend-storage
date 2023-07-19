#!/usr/bin/env python3
''' Exercise module '''
from typing import Union, Optional, Callable
import redis
import uuid
from functools import wraps


def call_history(method: Callable) -> Callable:
    """ store the history of inputs and outputs for a particular function """
    key = method.__qualname__
    inputs = key + ":inputs"
    outputs = key + ":outputs"

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ wrapped function """
        self._redis.rpush(inputs, str(args))
        data = method(self, *args, **kwds)
        self._redis.rpush(outputs, str(data))
        return data
    return wrapper


def count_calls(method: Callable) -> Callable:
    """ to count how many times methods of the Cache class are called """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ wrapped function """
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


class Cache:
    ''' Cache class '''
    def __init__(self):
        ''' initialize Class '''
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        ''' method that stores key-value pairs '''
        id: str = str(uuid.uuid4())
        self._redis.set(id, data)
        return id

    def get(self, key, fn: Optional[Callable]
            = None) -> Union[bytes, int, str, float]:
        ''' getter method for stored pairs '''
        val: bytes = self._redis.get(key)
        if fn is not None:
            val = fn(val)
        return val

    def get_str(self, key: str) -> str:
        ''' getter for str '''
        return self._redis.get(key, str)

    def get_int(self, key: str) -> int:
        ''' getter for int '''
        return self._redis.get(key, int)
