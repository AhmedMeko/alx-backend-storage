import redis
import uuid
from typing import Union, Callable, Optional, Any

class Cache:
    def __init__(self) -> None:
        # Initialize the Redis client and flush the database
        self._redis = redis.Redis()
        self._redis.flushdb()

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

# Example usage
if __name__ == "__main__":
    cache = Cache()

    # Store a string
    key1 = cache.store("Hello, Redis!")
    print(f"Stored string with key: {key1}")

    # Store an integer
    key2 = cache.store(123)
    print(f"Stored integer with key: {key2}")

    # Retrieve the stored string
    retrieved_str = cache.get_str(key1)
    print(f"Retrieved string: {retrieved_str}")

    # Retrieve the stored integer
    retrieved_int = cache.get_int(key2)
    print(f"Retrieved integer: {retrieved_int}")
