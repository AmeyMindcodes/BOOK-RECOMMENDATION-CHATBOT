import functools
import time
import json
import hashlib

# Simple in-memory cache
_cache = {}

def cache_result(timeout=3600):
    """
    Cache the result of a function call for a specified time.
    
    Args:
        timeout (int): Cache timeout in seconds (default: 1 hour)
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Create a cache key from the function name and arguments
            key_parts = [func.__name__]
            key_parts.extend([str(arg) for arg in args])
            key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
            key_str = json.dumps(key_parts)
            cache_key = hashlib.md5(key_str.encode()).hexdigest()
            
            # Check if the result is in the cache and not expired
            current_time = time.time()
            if cache_key in _cache:
                result, timestamp = _cache[cache_key]
                if current_time - timestamp < timeout:
                    return result
            
            # Call the function and cache the result
            result = func(*args, **kwargs)
            _cache[cache_key] = (result, current_time)
            
            return result
        return wrapper
    return decorator 