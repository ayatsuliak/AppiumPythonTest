import redis
import json
from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB


redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)


def cache_results(results):
    """Stores results in Redis for 1 hour."""
    for date, data in results.items():
        key = f"results:{date}"
        redis_client.setex(key, 3600, json.dumps(data))


def get_cached_results():
    """Retrieves cached results from Redis."""
    keys = redis_client.keys("results:*")
    return {key.replace("results:", ""): json.loads(redis_client.get(key)) for key in keys}
