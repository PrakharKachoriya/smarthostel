import asyncio
from collections import defaultdict
from typing import Any, AsyncGenerator, Dict, List
from functools import lru_cache

class PubSub:
    def __init__(self):
        self._subscribers: Dict[str, List[asyncio.Queue]] = defaultdict(list)

    async def subscribe(self, topic: str) -> AsyncGenerator[Any, None]:
        queue = asyncio.Queue()
        self._subscribers[topic].append(queue)
        try:
            while True:
                yield await queue.get()
        finally:
            self._subscribers[topic].remove(queue)

    async def publish(self, topic: str, message: Any):
        if topic in self._subscribers:
            for queue in self._subscribers[topic]:
                await queue.put(message)

@lru_cache
def get_pub_sub() -> PubSub:
    """Singleton instance of PubSub."""
    return PubSub()