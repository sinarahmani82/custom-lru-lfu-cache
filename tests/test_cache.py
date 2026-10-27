import pytest
from src.lru_cache import LRUCache
from src.lfu_cache import LFUCache

def test_lru_eviction_policy():
    """Verify that LRU strictly evicts the least recently accessed item."""
    cache = LRUCache(capacity=2)
    cache.put("a", 1)
    cache.put("b", 2)
    assert cache.get("a") == 1  # Key 'a' is accessed, making 'b' the oldest

    cache.put("c", 3)  # Eviction should drop 'b'
    assert cache.get("b") is None
    assert cache.get("a") == 1
    assert cache.get("c") == 3

def test_lfu_eviction_policy():
    """Verify that LFU evicts the item with lowest cumulative access frequency."""
    cache = LFUCache(capacity=2)
    cache.put("x", 10)
    cache.put("y", 20)

    # Access key 'x' twice
    cache.get("x")
    cache.get("x")

    # Access key 'y' once
    cache.get("y")

    # Inserting key 'z' must evict 'y' due to lower frequency
    cache.put("z", 30)
    assert cache.get("y") is None
    assert cache.get("x") == 10
    assert cache.get("z") == 30

def test_cache_hit_ratio_calculation():
    """Verify hit ratio statistical tracking accuracy."""
    cache = LRUCache(capacity=2)
    cache.put(1, "one")
    cache.get(1)  # Hit
    cache.get(2)  # Miss
    assert cache.hit_ratio() == 0.5
