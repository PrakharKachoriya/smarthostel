from app.logger import AppLogger

logger = AppLogger().get_logger()

def get_sql_insert_query_params(
    schema: str,
    table: str,
    obj: dict,
    return_values: list[str] = ['id']
) -> tuple[str, dict]:
    """Generate SQL query from a dictionary of parameters."""
    
    logger.debug(f"Generating SQL insert query for {schema}.{table} with data: {obj}")
    
    params = {k: v for k, v in obj.items() if v is not None}
    fields = ', '.join(params.keys())
    placeholders = ', '.join(f":{k}" for k in params.keys())
    
    query = f"""
        INSERT INTO {schema}.{table} ({fields})
        VALUES ({placeholders})
        RETURNING {', '.join(return_values)};
    """
    
    logger.debug(f"Generated SQL query: {query} with params: {params}")
    
    return query, params