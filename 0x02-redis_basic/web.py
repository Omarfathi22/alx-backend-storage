#!/usr/bin/env python3 
"""Module for an expiring web cache using Redis."""

import redis
import requests
from typing import Callable
from functools import wraps


redis_client = redis.Redis()

def wrap_requests(fn: Callable) -> Callable:
    """Decorator to cache HTTP GET requests in Redis."""
    
    @wraps(fn)
    def wrapper(url: str) -> str:
        """
        Handles caching logic for requests.

        Increments the request count in Redis, checks for a cached response,
        and returns it if available. If not cached, it makes the request,
        caches the response, and sets an expiration time.

        :param url: The URL to request.
        :return: The response text from the cached or fetched request.
        """
        
        redis_client.incr(f"count:{url}")
        
        
        cached_response = redis_client.get(f"cached:{url}")
        if cached_response:
            return cached_response.decode('utf-8')
        
        
        result = fn(url)
        
        
        redis_client.setex(f"cached:{url}", 10, result)
        return result

    return wrapper

@wrap_requests
def get_page(url: str) -> str:
    """Fetch the content of a webpage.

    Makes an HTTP GET request to the specified URL and returns the content.
    
    :param url: The URL of the page to retrieve.
    :return: The HTML content of the page.
    """
    response = requests.get(url)
    return response.text
