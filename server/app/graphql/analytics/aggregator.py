import asyncio

from contextlib import asynccontextmanager

from app.business.definitions.read import get_tenants as get_tenants_data
from app.core.trigger_queue import get_trigger_queue
from app.logger import AppLogger

logger = AppLogger().get_logger()

trigger_queue = get_trigger_queue()

async def handle_trigger(payload: dict):
    """Handle the trigger payload."""
    logger.debug(f"Handling trigger payload: {payload}")
    
    async def task_1():
        logger.debug("Task 1 started")
        res = [{**row} async for row in get_tenants_data()]
        logger.debug(f"Task 1 completed with result: {res}")
    
    async def task_2():
        logger.debug("Task 2 started")
        res = [{**row} async for row in get_tenants_data()]
        logger.debug(f"Task 2 completed with result: {res}")
    
    async def task_3():
        logger.debug("Task 3 started")
        res = [{**row} async for row in get_tenants_data()]
        logger.debug(f"Task 3 completed with result: {res}")
    
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(task_1())
            tg.create_task(task_2())
            tg.create_task(task_3())
        logger.debug("All tasks completed successfully")
    except asyncio.CancelledError:
        logger.error("Tasks were cancelled")
    except Exception as e:
        logger.error(f"Error handling trigger payload: {e}")
        return None
    

@asynccontextmanager
async def lifespan(app):
    # Start the trigger queue worker
    trigger_queue.start(handle_trigger)
    logger.info("Trigger queue started")

    yield  # Run the app

    # On shutdown, stop the worker
    await trigger_queue.stop()
    logger.info("Trigger queue stopped")