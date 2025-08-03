from datetime import date
from typing import Optional, Any

from app.core.database import get_db_manager
from app.config import DB_URL
from app.logger import AppLogger

logger = AppLogger().get_logger()


async def get_mealpending_data(
    pg_id: str,
    meal_type: str,
    date: date = date.today()
):
    query = """
        WITH tenants AS (
            SELECT id AS tenant_id
            FROM core.tenant
            WHERE PG_ID = :pg_id
        )
        
        , meal_activity AS (
            SELECT tenant_id
            FROM mess.daily_scans
            WHERE PG_ID = :pg_id
                AND meal_type = :meal_type
                AND curr_date = CURRENT_DATE
        )
        
        , combined AS (
            SELECT
                t.tenant_id
                , m.tenant_id AS meal_tenant_id
                , (
                    CASE
                    WHEN m.tenant_id IS NULL
                        THEN 'pending'
                    ELSE 'served'
                    END
                ) AS status
            FROM tenants t
            LEFT JOIN meal_activity m
            ON t.tenant_id = m.tenant_id
        )
        
        , status_counts AS (
            SELECT
                status
                , COUNT(*) AS value_counts
            FROM combined
            GROUP BY status
        )
        
        SELECT
            s.status AS status
            , COALESCE(sc.value_counts, 0) AS value_counts
        FROM (VALUES ('served'), ('pending')) AS s(status)
        LEFT JOIN status_counts sc ON (
            sc.status = s.status
        )
    """
    
    params = {
        "pg_id": pg_id,
        "meal_type": meal_type,
        # "date": date
    }
    
    db_manager = get_db_manager(DB_URL)
    try:
        rows = await db_manager.execute(query, params)
        for row in rows:
            yield row
    except Exception as e:
        print(f"Error fetching meal pending data: {e}")
        yield {}
    
    
async def get_floorwisecount_data(
    pg_id: str,
    meal_type: str,
    floor_number: int,
    date: str = "CURRENT_DATE"
):
    query = f"""
        WITH tenants AS (
            SELECT 
                id AS tenant_id
                , room_number
            FROM core.tenant
            WHERE PG_ID = :pg_id
                AND room_number LIKE ':floor_number%'
        )
            
        , meal_activity AS (
            SELECT tenant_id
            FROM mess.daily_scans
            WHERE PG_ID = :pg_id
                AND meal_type = :meal_type
                AND curr_date = CURRENT_DATE
        )
        
        , combined AS (
            SELECT
                t.tenant_id,
                t.room_number,
                (
                    CASE
                    WHEN m.tenant_id IS NULL
                        THEN 'pending'
                    ELSE 'served'
                    END
                ) AS status
            FROM tenants t
            LEFT JOIN meal_activity m
            ON t.tenant_id = m.tenant_id
        )

        room_status_counts AS (
            SELECT
                room_number,
                status,
                COUNT(*) AS count
            FROM combined
            GROUP BY room_number, status
        ),

        room_list AS (
            SELECT DISTINCT room_number FROM tenants
        ),

        status_list AS (
            SELECT unnest(ARRAY['pending', 'served']) AS status
        ),

        room_status_matrix AS (
            SELECT 
                rl.room_number,
                sl.status
            FROM room_list rl
            CROSS JOIN status_list sl
        )

        SELECT
            rsm.room_number,
            rsm.status,
            COALESCE(rsc.count, 0) AS value_counts
        FROM room_status_matrix rsm
        LEFT JOIN room_status_counts rsc
            ON rsm.room_number = rsc.room_number AND rsm.status = rsc.status
        ORDER BY rsm.room_number, rsm.status;
    """
    
    params = {
        "pg_id": pg_id,
        "meal_type": meal_type,
        "floor_number": floor_number,
    }
    
    db_manager = get_db_manager(DB_URL)
    try:
        rows = await db_manager.execute(query, params)
        for row in rows:
            yield row
    except Exception as e:
        print(f"Error fetching floor wise data: {e}")
        yield {}


async def get_table_data(
    pg_id: str,
    schema: str,
    table: str,
    and_filters: Optional[dict[str, Any]] = None,
):
    query = f"""
        SELECT *
        FROM {schema}.{table}
        WHERE pg_id = :pg_id
    """

    params = {
        "pg_id": pg_id
    }

    if and_filters:
        filter_clauses = []
        for idx, (col, val) in enumerate(and_filters.items()):
            param_key = f"filter_{idx}"
            filter_clauses.append(f"{col} = :{param_key}")
            params[param_key] = val
        query += " AND " + " AND ".join(filter_clauses)

    db_manager = get_db_manager(DB_URL)
    try:
        result = await db_manager.execute(query, params)
        for row in result:
            yield row
    except Exception as e:
        logger.error(f"Error printing all tenants {e}")
        yield {}


async def get_table_row(
    pg_id: str,
    schema: str,
    table: str,
    and_filters: Optional[dict[str, Any]] = None,
):
    query = f"""
        SELECT *
        FROM {schema}.{table}
        WHERE pg_id = :pg_id
    """

    params = {
        "pg_id": pg_id
    }

    if and_filters:
        filter_clauses = []
        for idx, (col, val) in enumerate(and_filters.items()):
            param_key = f"filter_{idx}"
            filter_clauses.append(f"{col} = :{param_key}")
            params[param_key] = val
        query += " AND " + " AND ".join(filter_clauses)


    db_manager = get_db_manager(DB_URL)
    try:
        result = await db_manager.execute(query, params, fetch="one")
        return result
    except Exception as e:
        logger.error(f"Error printing all tenants {e}")
        return {}