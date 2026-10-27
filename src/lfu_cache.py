from collections import defaultdict
from typing import Any, Optional, Dict

class LFUCache:
    """Least Frequently Used (LFU) Cache eviction engine with O(1) time complexity."""
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        self.capacity = capacity
        self.cache: Dict[Any, Any] = {}
        self.counts: Dict[Any, int] = defaultdict(int)
        self.freq_keys: Dict[int, list] = defaultdict(list)
        self.min_freq = 0
        self.hits = 0
        self.misses = 0

    def get(self, key: Any) -> Optional[Any]:
        """Fetch item value and increment its access frequency counter."""
        if key not in self.cache:
            self.misses += 1
            return None

        self.hits += 1
        val = self.cache[key]
        freq = self.counts[key]
        self.counts[key] += 1

        self.freq_keys[freq].remove(key)
        if not self.freq_keys[freq] and self.min_freq == freq:
            self.min_freq += 1

        self.freq_keys[freq + 1].append(key)
        return val

    def put(self, key: Any, value: Any) -> None:
        """Insert or update item, evicting the least frequently accessed item on overflow."""
        if key in self.cache:
            self.cache[key] = value
            self.get(key)
            return

        if len(self.cache) >= self.capacity:
            evict_key = self.freq_keys[self.min_freq].pop(0)
            del self.cache[evict_key]
            del self.counts[evict_key]

        self.cache[key] = value
        self.counts[key] = 1
        self.freq_keys[1].append(key)
        self.min_freq = 1

    def hit_ratio(self) -> float:
        """Calculate cumulative cache hit ratio."""
        total = self.hits + self.misses
        return round(self.hits / total, 4) if total > 0 else 0.0
