def get_sql_insert_query_params(schema: str, table: str, obj: dict) -> tuple[str, dict]:
    """Generate SQL query from a dictionary of parameters."""
    
    params = {k: v for k, v in obj.items() if v is not None}
    fields = ', '.join(params.keys())
    placeholders = ', '.join(f":{k}" for k in params.keys())
    
    query = f"""
        INSERT INTO {schema}.{table} ({fields})
        VALUES ({placeholders})
        RETURNING id;
    """
    
    return query, params