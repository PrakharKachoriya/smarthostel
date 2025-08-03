from app.logger import AppLogger
from app.config import DB_URL
from app.core.database import get_db_manager
from app.features.users.staff.models import CreateStaff
from app.features.shared.utils import get_sql_insert_query_params


logger = AppLogger().get_logger()

async def add_staff_service(
    data: CreateStaff,
    pg_id: str
):
    query, params = get_sql_insert_query_params(
        schema="core",
        table="staff",
        obj={**data.model_dump(), "pg_id": pg_id},
        return_values=["id", "pg_id", "name"]
    )

    db_manager = get_db_manager(DB_URL)

    try:
        # logger.info(f"Executing SQL query")
        result = await db_manager.execute(query, params, fetch="one", transactional=True)
        # logger.debug(f"Query executed successfully, result: {result}")
        return result
    except Exception as e:
        print(f"Error adding new tenant: {e}")
        return None