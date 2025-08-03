from app.logger import AppLogger
from app.config import DB_URL
from app.core.database import get_db_manager
from app.features.shared.utils import get_sql_insert_query_params
from app.features.users.admin.models import CreatePg


logger = AppLogger().get_logger()

async def add_pg_service(
    data: CreatePg,
):
    query, params = get_sql_insert_query_params(
        schema="core",
        table="pg",
        obj=data.model_dump(),
        return_values=["id", "name"]
    )
    logger.info(f"Adding new pg data: {params}")

    db_manager = get_db_manager(DB_URL)

    try:
        result = await db_manager.execute(query, params, fetch="one", transactional=True)
        return result
    except Exception as e:
        print(f"Error adding new tenant: {e}")
        return None