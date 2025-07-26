import asyncio
from typing import Callable
from abc import ABC, abstractmethod
from functools import lru_cache
from app.logger import AppLogger

logger = AppLogger().get_logger()

class TriggerQueue(ABC):
    def __init__(self):
        logger.debug("Initializing TriggerQueue")
        self._queue = asyncio.Queue()
        self._shutdown = asyncio.Event()
    
    def is_off(self):
        # logger.debug("Checking if TriggerQueue is off")
        return self._shutdown.is_set()
    
    async def enqueue(self, payload: dict):
        """Enqueue a payload to the trigger queue."""
        logger.debug(f"Enqueuing payload: {payload}")
        if not self.is_off():
            await self._queue.put(payload)
    
    @abstractmethod
    def start(self, handler: Callable):
        pass
    
    @abstractmethod
    async def stop(self):
        pass


class SingleWorkerTriggerQueue(TriggerQueue):
    def __init__(self):
        super().__init__()
        self._worker: asyncio.Task | None = None
    
    def start(self, handler: Callable):
        """Start the worker to process tasks from the queue."""
        logger.debug("Starting SingleWorkerTriggerQueue worker")
        if not self._worker or self._worker.done():
            self._shutdown.clear()
            logger.debug("Creating new worker task")
            self._worker = asyncio.create_task(self._run(handler))
    
    async def stop(self):
        logger.debug("Stopping SingleWorkerTriggerQueue worker")
        self._shutdown.set()
        if self._worker:
            logger.debug("Cancelling worker task")
            self._worker.cancel()
            try:
                await self._worker
            except asyncio.CancelledError:
                logger.error("Worker Cancelled")
                
            self._worker = None
    
    async def _run(self, handler: Callable):
        try:
            while not self.is_off():
                task = asyncio.wait_for(self._queue.get(), timeout=1) # Fetch task with a timeout
                try:
                    task = await task
                    logger.debug(f"Processing task: {task}")
                    await handler(task)
                except asyncio.TimeoutError:
                    continue # Check for shutdown every second
        except asyncio.CancelledError:
            logger.error("TriggerQueue worker cancelled")


class MultiWorkerTriggerQueue(TriggerQueue):
    def __init__(
        self,
        concurrency: int = 4,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        super().__init__()
        self._concurrency = concurrency
        self._max_retries = max_retries
        self._retry_delay = retry_delay
        self._workers = list[asyncio.Task] = []
    
    def start(self, handler: Callable):
        for _ in range(self._concurrency):
            worker = asyncio.create_task(self._worker_loop(handler, _+1))
            self._workers.append(worker)
    
    async def stop(self):
        self._shutdown.set()
        for worker in self._workers:
            worker.cancel()
            try:
                await worker
            except asyncio.CancelledError:
                print(f"Worker Cancelled")
            
            worker = None
    
    async def _worker_loop(self, handler: Callable, worker_id: int):
        while not self.is_off():
            task = asyncio.wait_for(self._queue.get(), timeout=1) # Fetch task with a timeout
            try:
                await self._process_with_retries(task, handler, worker_id)
            except asyncio.TimeoutError:
                continue # Check for shutdown every second
            except asyncio.CancelledError:
                print("MultiWorkerTriggerQueue worker cancelled")
    
    async def _process_with_retries(
        self,
        task: dict,
        handler: Callable,
        worker_id: int
    ):
        for attempt in range(1, self._max_retries + 2):
            try:
                await handler(task)
                return
            except Exception as e:
                print(f"Worker {worker_id} failed to process task {task} on attempt {attempt}: {e}")
                if attempt > self._max_retries:
                    print(f"Worker {worker_id} giving up on task {task} after {self._max_retries} retries")
                    break
                await asyncio.sleep(self._retry_delay * attempt)


@lru_cache
def get_trigger_queue(
    queue_type: str = "single",
    concurrency: int = 4,
    max_retries: int = 3,
    retry_delay: float = 1.0
) -> TriggerQueue:
    """Factory function to get a TriggerQueue instance."""
    if queue_type == "single":
        return SingleWorkerTriggerQueue()
    elif queue_type == "multi":
        return MultiWorkerTriggerQueue(concurrency, max_retries, retry_delay)
    else:
        raise ValueError(f"Unknown queue type: {queue_type}")
