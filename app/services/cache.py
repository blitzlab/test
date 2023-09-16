import cachetools

from core.config import settings

# Define the cache and its size
cache = cachetools.LRUCache(maxsize=settings.CACHE_MAX_SIZE)

def get_from_cache(key):
    return cache.get(key)

def set_to_cache(key, value, ttl=settings.CACHE_TTL):
    # In cachetools v5.0.0+, you can use cache.set() with a ttl
    cache[key] = value
    return value

def delete_from_cache(key):
    cache.pop(key, None)
