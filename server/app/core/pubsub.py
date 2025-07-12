import asyncio
from typing import Callable
from abc import ABC, abstractmethod

class PubSubQueue(ABC):
    def __init__(self):
        self._queue = asyncio.Queue()
        self._shutdown = asyncio.Event()
    
    def is_off(self):
        return self._shutdown.is_set()
    
    async def enqueue(self, payload: dict):
        if not self.is_off():
            await self._queue.put(payload)
    
    @abstractmethod
    def start(self, handler: Callable):
        pass
    
    @abstractmethod
    async def stop(self):
        pass


class SingleWorkerPubSubQueue(PubSubQueue):
    def __init__(self):
        super().__init__()
        self._worker = asyncio.Task | None = None
    
    def start(self, handler: Callable):
        if not self._worker:
            self._worker = asyncio.create_task(self._run(handler))
    
    async def stop(self):
        self._shutdown.set()
        if self._worker:
            self._worker.cancel()
            try:
                await self._worker
            except asyncio.CancelledError:
                print("Worker Cancelled")
                
            self._worker = None
    
    
    
    async def _run(self, handler: Callable):
        try:
            while not self.is_off():
                task = asyncio.wait_for(self._queue.get(), timeout=1) # Fetch task with a timeout
                try:
                    await handler(task)
                except asyncio.TimeoutError:
                    continue # Check for shutdown every second
        except asyncio.CancelledError:
            print("PubSubQueue worker cancelled")


class MultiWorkerPubSubQueue(PubSubQueue):
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
                print("MultiWorkerPubSubQueue worker cancelled")
    
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
