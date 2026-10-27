from typing import Any, Optional, Dict

class Node:
    """Doubly linked list node holding key-value pairs."""
    def __init__(self, key: Any, value: Any):
        self.key = key
        self.value = value
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None

class LRUCache:
    """Least Recently Used (LRU) Cache eviction engine with strict O(1) runtime."""
    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be a positive integer.")
        self.capacity = capacity
        self.cache: Dict[Any, Node] = {}
        self.hits = 0
        self.misses = 0

        # Dummy sentinel nodes to eliminate null-check edge cases
        self.head = Node(0, 0)
        self.tail = Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        """Unlink an existing node from the doubly linked list in O(1)."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_head(self, node: Node) -> None:
        """Insert a node right after head sentinel (marks as most recently used) in O(1)."""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node

    def get(self, key: Any) -> Optional[Any]:
        """Retrieve key value and promote node to most recently used position."""
        if key in self.cache:
            self.hits += 1
            node = self.cache[key]
            self._remove(node)
            self._add_to_head(node)
            return node.value
        self.misses += 1
        return None

    def put(self, key: Any, value: Any) -> None:
        """Insert or update key-value pair, evicting the LRU item if capacity is exceeded."""
        if key in self.cache:
            node = self.cache[key]
            node.value = value
            self._remove(node)
            self._add_to_head(node)
        else:
            if len(self.cache) >= self.capacity:
                # Evict the least recently used node (immediately before tail sentinel)
                lru_node = self.tail.prev
                self._remove(lru_node)
                del self.cache[lru_node.key]

            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)

    def hit_ratio(self) -> float:
        """Calculate cumulative cache hit ratio."""
        total = self.hits + self.misses
        return round(self.hits / total, 4) if total > 0 else 0.0
