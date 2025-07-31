from app.core.database import get_db_manager
from app.core.utils import get_sql_insert_query_params
from app.config import DB_URL
from app.logger import AppLogger
from app.business.definitions.types import (
    CreateTenant, CreatePg, CreateStaff, CreateQRScanLog
)

logger = AppLogger().get_logger()

async def add_new_tenant(
    data: CreateTenant,
    pg_id: str
):
    
    query, params = get_sql_insert_query_params(
        schema="core",
        table="tenant",
        obj={**data.model_dump(), "pg_id": pg_id},
        return_values=["id", "pg_id", "name"]
    )
    
    db_manager = get_db_manager(DB_URL)
    
    try:
        logger.info(f"Executing SQL query")
        result = await db_manager.execute(query, params, fetch="one", transactional=True)
        logger.debug(f"Query executed successfully, result: {result}")
        return result
    except Exception as e:
        print(f"Error adding new tenant: {e}")
        return None

async def add_new_staff(
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
        logger.info(f"Executing SQL query")
        result = await db_manager.execute(query, params, fetch="one", transactional=True)
        logger.debug(f"Query executed successfully, result: {result}")
        return result
    except Exception as e:
        print(f"Error adding new tenant: {e}")
        return None
    
async def add_new_pg(
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


async def add_new_qr_scan_log(
    pg_id: str,
    data: CreateQRScanLog
):
    
    query, params = get_sql_insert_query_params(
        schema="mess",
        table="daily_scans",
        obj=data.model_dump(),
        return_values=["id", "pg_id", "tenant_id", "meal_type"]
    )
    logger.info(f"Adding new QR scan log for pg {pg_id} with data: {params}")
    
    db_manager = get_db_manager(DB_URL)
    try:
        result = await db_manager.execute(query, params, fetch="none", transactional=True)
        return result
    except Exception as e:
        print(f"Error printing all tenants {e}")
        return None