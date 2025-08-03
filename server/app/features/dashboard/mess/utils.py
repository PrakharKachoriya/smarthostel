from datetime import date

from app.core.trigger_queue import get_trigger_queue


trigger_queue = get_trigger_queue(queue_type="multi")

async def trigger_dashboard_workers(pg_id: str, meal_type: str):
    trigger_payload = {
        "action": f"qr scanned on {date.today()} in PG: {pg_id} at {meal_type}",
        "pg_key": pg_id,
        "meal_type": meal_type
    }

    await trigger_queue.enqueue(trigger_payload)