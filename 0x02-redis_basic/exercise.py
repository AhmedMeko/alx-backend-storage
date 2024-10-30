import redis
import uuid
from typing import Union

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
