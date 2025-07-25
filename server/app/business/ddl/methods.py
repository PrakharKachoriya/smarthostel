from app.business.ddl.queries import create_schema_if_not_exists, create_table_if_not_exists
from app.core.database import get_db_manager
from app.config import DB_URL

async def create_schema_if_not_exists(schema: str) -> None:
    query = create_schema_if_not_exists(schema)
    db_manager = get_db_manager(DB_URL)
    try:
        await db_manager.execute(query)
    except Exception as e:
        print(f"Error creating schema {schema}: {e}")

async def create_table_if_not_exists(schema: str, table: str, columns: list[str]) -> None:
    query = create_table_if_not_exists(schema, table, columns)
    db_manager = get_db_manager(DB_URL)
    try:
        await db_manager.execute(query)
    except Exception as e:
        print(f"Error creating table {schema}.{table}: {e}")