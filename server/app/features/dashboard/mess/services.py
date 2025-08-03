from app.logger import AppLogger
from app.config import DB_URL
from app.core.database import get_db_manager
from app.features.shared.utils import get_sql_insert_query_params
from app.features.dashboard.mess.models import CreateQRScanLog


logger = AppLogger().get_logger()


async def add_qr_scan_log_service(
        pg_id: str,
        data: CreateQRScanLog
):
    query, params = get_sql_insert_query_params(
        schema="mess",
        table="daily_scans",
        obj={**data.model_dump(), "pg_id": pg_id},
        return_values=["id", "pg_id", "tenant_id", "meal_type"]
    )
    logger.info(f"Adding new QR scan log for pg {pg_id} with data: {params}")

    db_manager = get_db_manager(DB_URL)
    try:
        result = await db_manager.execute(query, params, fetch="one", transactional=True)
        return result
    except Exception as e:
        print(f"Error printing all tenants {e}")
        return None