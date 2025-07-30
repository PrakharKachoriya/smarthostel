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
    def __init__(self, worker_count: int = 4, max_retries: int = 3, backoff_base: float = 0.5):
        super().__init__()
        logger.debug(f"Initializing MultiWorkerTriggerQueue with {worker_count} workers")
        self._workers: list[asyncio.Task] = []
        self._worker_count = worker_count
        self._max_retries = max_retries
        self._backoff_base = backoff_base

    def start(self, handler: Callable):
        logger.debug(f"Starting {self._worker_count} workers")
        self._shutdown.clear()

        for worker_id in range(self._worker_count):
            task = asyncio.create_task(self._run(handler, worker_id))
            self._workers.append(task)

    async def stop(self):
        logger.debug("Stopping all workers")
        self._shutdown.set()

        for task in self._workers:
            task.cancel()

        for task in self._workers:
            try:
                await task
            except asyncio.CancelledError:
                logger.debug("Worker cancelled")

        self._workers = []

    async def _run(self, handler: Callable, worker_id: int):
        logger.debug(f"Worker-{worker_id} started")
        try:
            while not self.is_off():
                task = await self._queue.get()
                await self._handle_with_retry(handler, task, worker_id)
        except asyncio.CancelledError:
            logger.debug(f"Worker-{worker_id} cancelled")
        finally:
            logger.debug(f"Worker-{worker_id} stopped")

    async def _handle_with_retry(self, handler: Callable, task: dict, worker_id: int):
        attempt = 0
        while attempt <= self._max_retries:
            try:
                logger.debug(f"Worker-{worker_id} attempt {attempt+1} for task: {task}")
                await handler(task)
                return  # success
            except Exception as e:
                attempt += 1
                logger.warning(f"Worker-{worker_id} failed on attempt {attempt} with error: {e}")
                if attempt > self._max_retries:
                    logger.error(f"Worker-{worker_id} permanently failed task after {attempt} attempts: {task}")
                    return
                backoff_time = self._backoff_base * (2 ** (attempt - 1))
                await asyncio.sleep(backoff_time)


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
