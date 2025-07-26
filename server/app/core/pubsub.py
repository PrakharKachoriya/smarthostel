from functools import lru_cache
import asyncio
from typing import Dict, List, Any, AsyncGenerator
from collections import defaultdict

from app.logger import AppLogger

logger = AppLogger().get_logger()

class PubSub:
    def __init__(self):
        self._subscribers = None
        self._lock = None
    
    @property
    def subscribers(self):
        """Get the current subscribers."""
        if not self._subscribers:
            self._subscribers: Dict[str, List[asyncio.Queue]] = defaultdict(list)
        logger.debug(f"Current subscribers: {self._subscribers}")
        return self._subscribers
    
    @property
    def lock(self):
        """Acquire a lock for thread-safe operations."""
        logger.debug("Acquiring lock for PubSub operations")
        if not self._lock:
            self._lock = asyncio.Lock()
        return self._lock

    async def subscribe(self, topic: str) -> AsyncGenerator[Any, None]:
        queue = asyncio.Queue(maxsize=100)  # Bounded queue to avoid memory leaks
        async with self.lock:
            logger.debug(f"Subscribing to topic: {topic}")
            self.subscribers[topic].append(queue)

        try:
            while True:
                message = await queue.get()
                logger.debug(f"Received message on topic {topic}: {message}")
                yield message
        finally:
            async with self.lock:
                if queue in self.subscribers[topic]:
                    logger.debug(f"Unsubscribing from topic: {topic}")
                    self.subscribers[topic].remove(queue)
                    
                    # if list is empty, delete the topic
                    if not self.subscribers[topic]:
                        del self.subscribers[topic]

    async def publish(self, topic: str, message: Any):
        async with self.lock:
            logger.debug(f"Publishing message to topic {topic}: {message}")
            queues = list(self.subscribers.get(topic, []))  # shallow copy with references

        # Send the message to all subscriber queues (do NOT lock this part)
        for queue in queues:
            try:
                await queue.put(message)
            except asyncio.QueueFull:
                # Optionally log or drop the message for slow subscribers
                pass
        logger.debug(f"Message published to {len(queues)} subscribers on topic {topic}")

@lru_cache
def get_pub_sub() -> PubSub:
    """Singleton instance of PubSub."""
    return PubSub()