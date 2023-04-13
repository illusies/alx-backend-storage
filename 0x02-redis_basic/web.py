#!/usr/bin/env python3
"""A program that implements a get page function"""
import requests
import time
from functools import lru_cache

@lru_cache(maxsize=None)
def get_page(url: str) -> str:
    """
    A function that uses the requests module to obtain the HTML
    content of a particular URL and return it
    """
    count_key = f"count:{url}"
    count = int(cache.get(count_key, 0))
    cache.set(count_key, count + 1, ex=10)
    response = requests.get(url)
    return response.text
