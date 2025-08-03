from typing import Optional, Any

from app.config import DB_URL
from app.core.database import get_db_manager
from app.logger import AppLogger
from app.features.shared.utils import (
    create_schema_if_not_exists_query,
    create_table_if_not_exists_query
)


logger = AppLogger().get_logger()

async def get_table_data_by_pg(
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

async def get_table_row_by_pg(
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


async def delete_table_row(
    pg_id: str,
    schema: str,
    table: str,
    and_filters: Optional[dict[str, Any]] = None,
):
    query = f"""
        DELETE FROM
        {schema}.{table}
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


async def get_table_data_ext(
    schema: str,
    table: str,
    and_filters: Optional[dict[str, Any]] = None,
):
    query = f"""
        SELECT *
        FROM {schema}.{table}
    """

    params = {}

    if and_filters:
        filter_clauses = []
        for idx, (col, val) in enumerate(and_filters.items()):
            param_key = f"filter_{idx}"
            filter_clauses.append(f"{col} = :{param_key}")
            params[param_key] = val
        query += " WHERE " + " AND ".join(filter_clauses)

    db_manager = get_db_manager(DB_URL)
    try:
        result = await db_manager.execute(query, params)
        for row in result:
            yield row
    except Exception as e:
        logger.error(f"Error printing all tenants {e}")
        yield {}


async def get_table_row_ext(
    schema: str,
    table: str,
    and_filters: Optional[dict[str, Any]] = None,
):
    query = f"""
        SELECT *
        FROM {schema}.{table}
    """

    params = {}

    if and_filters:
        filter_clauses = []
        for idx, (col, val) in enumerate(and_filters.items()):
            param_key = f"filter_{idx}"
            filter_clauses.append(f"{col} = :{param_key}")
            params[param_key] = val
        query += " WHERE " + " AND ".join(filter_clauses)

    db_manager = get_db_manager(DB_URL)
    try:
        result = await db_manager.execute(query, params, fetch="one")
        return result
    except Exception as e:
        logger.error(f"Error printing all tenants {e}")
        return {}


async def create_schema_if_not_exists(schema: str) -> None:
    query = create_schema_if_not_exists_query(schema)
    db_manager = get_db_manager(DB_URL)
    try:
        await db_manager.run_ddl(query)
    except Exception as e:
        logger.error(f"Error creating schema {schema}: {e}")


async def create_table_if_not_exists(schema: str, table: str, columns: list[str]) -> None:
    query = create_table_if_not_exists_query(schema, table, columns)
    db_manager = get_db_manager(DB_URL)
    try:
        await db_manager.run_ddl(query)
    except Exception as e:
        logger.error(f"Error creating table {schema}.{table}: {e}")