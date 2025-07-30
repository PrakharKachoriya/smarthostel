from datetime import date

from app.core.database import get_db_manager
from app.config import DB_URL


async def get_mealpending_data(meal_type: str, date: date = date.today()):
    query = """
        WITH tenants AS (
            SELECT id AS tenant_id
            FROM master.tenants_dim
        )
        
        , meal_activity AS (
            SELECT tenant_id
            FROM analytics.meal_activity_fact
            WHERE meal_type = :meal_type AND timestamp::date = :date
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
                status,
                COUNT(*) AS value_counts
            FROM combined
            GROUP BY status
        )
        
        SELECT
            s.status AS status,
            COALESCE(sc.value_counts, 0) AS value_counts
        FROM (VALUES ('served'), ('pending')) AS s(status)
        LEFT JOIN status_counts sc ON (
            sc.status = s.status
        )
    """
    
    params = {
        "meal_type": meal_type,
        "date": date
    }
    
    db_manager = get_db_manager(DB_URL)
    try:
        rows = await db_manager.execute(query, params)
        for row in rows:
            yield row
    except Exception as e:
        print(f"Error fetching meal pending data: {e}")
        yield None
    
    
async def get_floorwisecount_data(
    meal_type: str,
    floor_number: int,
    date: str = "CURRENT_DATE"
):
    query = f"""
        WITH tenants AS (
            SELECT 
                id AS tenant_id,
                room_number,
            FROM master.tenants_dim
            WHERE room_number LIKE '{floor_number}%'
            )
            
        , meal_activity AS (
            SELECT tenant_id
            FROM analytics.meal_activity_fact
            WHERE
                meal_type = :meal_type
                AND timestamp::date = :date
                AND room_number LIKE '{floor_number}%'
        )
        
        , combined AS (
            SELECT
                t.tenant_id,
                t.room_number,
                t.floor,
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
        
        SELECT 
            room_number,
            COUNT(CASE WHEN status = 'served' THEN 1 END) AS served_count,
            COUNT(CASE WHEN status = 'pending' THEN 1 END) AS pending_count
        FROM combined
        GROUP BY room_number
    """
    
    params = {
        "meal_type": meal_type,
        "floor_number": floor_number,
        "date": date
    }
    
    db_manager = get_db_manager(DB_URL)
    try:
        result = await db_manager.execute(query, params)
        
        # format here
        room_numbers = [row["room_number"] for row in result]
        served = [row["served_count"] for row in result]
        pending = [row["pending_count"] for row in result]
        
        served_pending_tuples = []
        for s, p in zip(served, pending):
            new_type = (s, p)
            served_pending_tuples.append(new_type)

        return room_numbers, served_pending_tuples
    
    except Exception as e:
        print(f"Error fetching floor wise data: {e}")
        return None
    
    # [501, 502]
    # [1,2] s
    # [4, 3] p
    # for s, p in zip(served, pending):
        # new_type = (s, p)
        # new_list.append(new_type)
        
    

async def get_mealtime_data(meal_type:str, date: str = 'CURRENT_DATE'):
    query = """
        WITH time_data AS (
            SELECT tenant_id, TO_CHAR(timestamp::time, 'HH24:MI' ) AS time_value 
            FROM analytics.meal_activity_fact
            WHERE meal_type = :meal_type AND timestamp::date = :date
        )
        
        SELECT time_value, COUNT(tenant_id) AS value_counts
        FROM time_data
        GROUP BY time_value
    """
    
    params = {
        "meal_type": meal_type,
        "date": date
    }
    
    db_manager = get_db_manager(DB_URL)
    try:
        rows = await db_manager.execute(query, params)
        for row in rows:
            yield row
    except Exception as e:
        print(f"Error fetching meal time line chart data: {e}")
        yield None

async def get_foodrating_data(meal_type: str, date: str = "CURRENT_DATE"):
    query = """
        WITH ratings AS (
            SELECT tenant_id, rating
            FROM analytics.meal_activity_fact
            WHERE meal_type = :meal_type AND timestamp::date = :date
        )
        
        SELECT rating, COUNT(tenant_id) AS value_counts
        FROM ratings
        GROUP BY rating
    """
    
    params = {
        "meal_type": meal_type,
        "date": date
    }
    
    db_manager = get_db_manager(DB_URL)
    try:
        rows = await db_manager.execute(query, params)
        for row in rows:
            yield row
    except Exception as e:
        print(f"Error fetching food rating data: {e}")
        yield None


async def get_tenants():
    query = """
        SELECT *
        FROM core.tenant
    """
    db_manager = get_db_manager(DB_URL)
    try:
        result = await db_manager.execute(query)
        for row in result:
            yield row
    except Exception as e:
        print(f"Error printing all tenants {e}")
        yield None


async def get_mealactivity():
    query = """
        SELECT *
        FROM analytics.meal_activity_fact
    """
    db_manager = get_db_manager(DB_URL)
    try:
        result = await db_manager.execute(query)
        for row in result:
            yield row
    except Exception as e:
        print(f"Error printing all tenants {e}")
        yield None


async def get_table_data(
    schema: str,
    table: str
):
    query = f"""
        SELECT *
        FROM {schema}.{table}
    """
    db_manager = get_db_manager(DB_URL)
    try:
        result = await db_manager.execute(query)
        for row in result:
            yield row
    except Exception as e:
        print(f"Error printing all tenants {e}")
        yield None