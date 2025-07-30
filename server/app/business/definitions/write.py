from app.core.database import get_db_manager
from app.core.utils import get_sql_insert_query_params
from app.config import DB_URL
from app.logger import AppLogger
from app.business.definitions.types import CreateTenant

logger = AppLogger().get_logger()

async def add_new_tenant(
    data: CreateTenant,
    pg_id: str
):
    # query = """
    #     INSERT INTO core.tenants (pg_id, name, email, phone_number, room_number, join_date) VALUES (
    #         :pg_id, :name, :email, :phone_number, :room_number, COALESCE(:join_date, CURRENT_DATE)
    #     )
    # """
    # params = {
    #     "pg_id": pg_id,
    #     "name": name,
    #     "email": email,
    #     "phone_number": phone_number,
    #     "room_number": room_number,
    #     "join_date": join_date
    # }
    
    query, params = get_sql_insert_query_params(
        schema="core",
        table="tenants",
        obj=data.model_dump()
    )
    params["pd_id"] = pg_id
    logger.info(f"Adding to pg {params["pd_id"]} - tenant data: {params}")
    
    db_manager = get_db_manager(DB_URL)
    
    try:
        result = await db_manager.execute(query, params, fetch="one", transactional=True)
        return result
    except Exception as e:
        print(f"Error adding new tenant: {e}")
        return None


async def add_new_mealactivity(
    tenant_id: str,
    meal_type: str,
    room_number: int | None = None,
    timestamp: float | None = None,
    rating: int | None = None
):
    logger.info(f"Adding new meal activity for tenant {tenant_id}, room {room_number}, meal type {meal_type}, timestamp {timestamp}, rating {rating}")
    
    query = """
        INSERT INTO analytics.meal_activity_fact (tenant_id, room_number, meal_type, timestamp, rating) VALUES (
            :tenant_id, :room_number, :meal_type, CURRENT_TIMESTAMP, NULL
        )
    """
    params = {
        "tenant_id": tenant_id,
        "room_number": room_number,
        "meal_type": meal_type,
    }
    
    db_manager = get_db_manager(DB_URL)
    try:
        result = await db_manager.execute(query, params, fetch="none", transactional=True)
        return result
    except Exception as e:
        print(f"Error printing all tenants {e}")
        return None