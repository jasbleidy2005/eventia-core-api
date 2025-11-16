import redis
import json
from src.config.settings import Config

class RedisClient:
    _instance = None
    
    def __init__(self):
        self.client = redis.Redis(
            host=Config.REDIS_HOST,
            port=Config.REDIS_PORT,
            decode_responses=True
        )
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def get(self, key):
        value = self.client.get(key)
        return json.loads(value) if value else None
    
    def set(self, key, value, expire=300):
        self.client.setex(key, expire, json.dumps(value))
    
    def delete(self, key):
        self.client.delete(key)