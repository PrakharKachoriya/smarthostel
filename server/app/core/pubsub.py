from functools import lru_cache
import asyncio
from typing import Dict, List, Any, AsyncGenerator
from collections import defaultdict

class PubSub:
    def __init__(self):
        self._subscribers: Dict[str, List[asyncio.Queue]] = defaultdict(list)
        self._lock = asyncio.Lock()

    async def subscribe(self, topic: str) -> AsyncGenerator[Any, None]:
        queue = asyncio.Queue(maxsize=100)  # Bounded queue to avoid memory leaks
        async with self._lock:
            self._subscribers[topic].append(queue)

        try:
            while True:
                message = await queue.get()
                yield message
        finally:
            async with self._lock:
                if queue in self._subscribers[topic]:
                    self._subscribers[topic].remove(queue)
                    if not self._subscribers[topic]:
                        del self._subscribers[topic]

    async def publish(self, topic: str, message: Any):
        async with self._lock:
            queues = list(self._subscribers.get(topic, []))  # shallow copy with queue references

        # Send the message to all subscriber queues (do NOT lock this part)
        for queue in queues:
            try:
                await queue.put(message)
            except asyncio.QueueFull:
                # Optionally log or drop the message for slow subscribers
                pass

@lru_cache
def get_pub_sub() -> PubSub:
    """Singleton instance of PubSub."""
    return PubSub()