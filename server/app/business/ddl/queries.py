from sqlalchemy.sql import quoted_name

# def create_schema_if_not_exists(schema: str) -> str:
#     return f"""
#         CREATE SCHEMA IF NOT EXISTS {schema};
#     """

# def create_table_if_not_exists(schema: str, table: str, columns: list[str]) -> str:
#     return f"""
#         CREATE TABLE IF NOT EXISTS {schema}.{table} (
#             {', '.join(columns)}
#         );
#     """


def create_schema_if_not_exists_query(schema: str) -> str:
    return f'CREATE SCHEMA IF NOT EXISTS "{quoted_name(schema, quote=True)}";'

def create_table_if_not_exists_query(schema: str, table: str, columns: list[str]) -> str:
    column_defs = ', '.join(columns)
    return f'CREATE TABLE IF NOT EXISTS "{quoted_name(schema, quote=True)}"."{quoted_name(table, quote=True)}" ({column_defs});'