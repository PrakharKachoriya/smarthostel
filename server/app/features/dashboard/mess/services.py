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


async def get_mealpending_data(
    pg_id: str,
    meal_type: str,
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
    }

    db_manager = get_db_manager(DB_URL)
    try:
        rows = await db_manager.execute(query, params)
        for row in rows:
            yield row
    except Exception as e:
        logger.error(f"Error fetching meal pending data: {e}")
        yield {}


async def get_distinct_floors_data(
    pg_id: str
):
    query = """
        SELECT DISTINCT
            floor
        FROM core.tenant
    """

    params = {
        "pg_id": pg_id
    }

    db_manager = get_db_manager(DB_URL)
    floors = []
    try:
        rows = await db_manager.execute(query, params)
        for row in rows:
            floors.append(row["floor"])
        return floors
    except Exception as e:
        logger.error(f"Error fetching floor wise data: {e}")
        return floors


async def get_floorwisecount_data(
    pg_id: str,
    meal_type: str,
    floor: int
):
    query = """
        WITH tenants AS (
            SELECT
                id AS tenant_id
                , floor
                , room_number
            FROM core.tenant
            WHERE PG_ID = :pg_id
                AND floor = :floor
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
        LEFT JOIN room_status_counts rsc ON (
            rsm.room_number = rsc.room_number 
            AND rsm.status = rsc.status
        )
    """

    params = {
        "pg_id": pg_id,
        "meal_type": meal_type,
        "floor": floor
    }

    db_manager = get_db_manager(DB_URL)
    try:
        rows = await db_manager.execute(query, params)
        for row in rows:
            yield row
    except Exception as e:
        logger.error(f"Error fetching floor wise data: {e}")
        yield {}