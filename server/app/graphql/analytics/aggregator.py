import asyncio

from contextlib import asynccontextmanager

from app.business.definitions.read import get_tenants as get_tenants_data
from app.business.definitions.read import get_mealpending_data, get_floorwisecount_data
from app.core.trigger_queue import get_trigger_queue
from app.core.pubsub import get_pub_sub
from app.logger import AppLogger

logger = AppLogger().get_logger()

trigger_queue = get_trigger_queue(queue_type="multi")
pubsub = get_pub_sub()

async def handle_trigger(payload: dict):
    """Handle the trigger payload."""
    logger.debug(f"Handling trigger payload: {payload}")
    
    async def task_1():
        topic = f"{payload["pg_key"]}_mealpending_piechart_{payload["meal_type"]}"
        logger.debug(f"Task started for {topic}")
        res = {
            "labels": [],
            "values": []
        }
        try:
            async for row in get_mealpending_data(payload["meal_type"]):
                res["labels"].append(row["status"])
                res["values"].append(row["value_counts"])
            
        except Exception as e:
            logger.error(f"Error fetching meal pending data: {e}")

        logger.debug(f"Task meal pending pie chart completed with result: {res}")
        try:
            await pubsub.publish(topic, res)
        except Exception as e:
            logger.error(f"Error publishing meal pending pie chart: {e}")
    

    async def task_2():
        topic = f"{payload["pg_key"]}__roomwise_count_5__{payload["meal_type"]}"
        logger.debug(f"Task started for {topic}")
        res = {}
        room_data = {}
        try:
            async for row in get_floorwisecount_data(payload["meal_type"], "5"):
                room = row["room_number"]
                status = row["status"]
                count = row["value_counts"]
                room_data[room][status] = count

                sorted_rooms = sorted(room_data.keys())

            # Prepare counts aligned with sorted rooms
            pending_counts = [room_data[room].get('pending', 0) for room in sorted_rooms]
            served_counts = [room_data[room].get('served', 0) for room in sorted_rooms]

            res = {
                "x": {"room_numbers": sorted_rooms},
                "y": {
                    "pending": pending_counts,
                    "served": served_counts
                }
            }
        except Exception as e:
            logger.error(f"Error fetching tenants data: {e}")
        
        logger.debug(f"Task tenants data completed with result: {res}")
        await pubsub.publish(topic, res)
    
    
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(task_1())
            tg.create_task(task_2())
            
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