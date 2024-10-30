import redis
import uuid
from typing import Union, Callable, Optional, Any
from functools import wraps

def count_calls(method: Callable) -> Callable:
    """Decorator to count how many times a method is called."""
    
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        # Generate a key using the qualified name of the method
        key = method.__qualname__
        
        # Increment the call count in Redis
        self._redis.incr(key)
        
        # Call the original method and return its result
        return method(self, *args, **kwargs)
    
    return wrapper

class Cache:
    def __init__(self) -> None:
        # Initialize the Redis client and flush the database
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        # Generate a random key
        key = str(uuid.uuid4())
        
        # Store the data in Redis using the random key
        self._redis.set(key, data)
        
        # Return the generated key
        return key

    def get(self, key: str, fn: Optional[Callable[[bytes], Any]] = None) -> Optional[Any]:
        # Retrieve the value from Redis
        value = self._redis.get(key)
        
        # If the key does not exist, return None (default behavior)
        if value is None:
            return None
        
        # If a function is provided, apply it to the value
        if fn:
            return fn(value)
        
        # Otherwise, return the raw value (bytes)
        return value

    def get_str(self, key: str) -> Optional[str]:
        return self.get(key, fn=lambda x: x.decode('utf-8'))

    def get_int(self, key: str) -> Optional[int]:
        return self.get(key, fn=lambda x: int(x))

    def get_call_count(self, method_name: str) -> int:
        """Retrieve the call count for a method."""
        return self._redis.get(method_name) or 0

# Example usage
if __name__ == "__main__":
    cache = Cache()

    # Store some data
    key1 = cache.store("Hello, Redis!")
    print(f"Stored string with key: {key1}")

    key2 = cache.store(123)
    print(f"Stored integer with key: {key2}")

    # Get call counts
    store_count = cache.get_call_count('Cache.store')
    print(f"'store' method has been called {store_count} times.")
