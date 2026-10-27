"""Custom LRU and LFU Cache Eviction Package."""
from .lru_cache import LRUCache
from .lfu_cache import LFUCache

__all__ = ["LRUCache", "LFUCache"]
