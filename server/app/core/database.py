from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection
from sqlalchemy.engine import Row
from sqlalchemy import text
from typing import Optional, Union, Dict, Any, Sequence, Literal
from functools import lru_cache

class DBManager:
    
    _instance = None
    def __init__(self, db_url: str) -> "DBManager":
        self.engine: AsyncEngine = create_async_engine(
            self.db_url,
            echo=True,
            pool_size=20,
            max_overflow=10,
            pool_timeout=30,
            pool_recycle=1800
        )
    
    async def execute(
        self,
        sql_query: str,
        params: Optional[Union[Dict[str, Any], Sequence[Dict[str, Any]]]] = None,
        fetch: Literal["all", "one", "none"] = "all",
        transactional: bool = False
    ) -> Union[None, Sequence[Dict[str, Any]], Dict[str, Any]]:
        """Executes a SQL query against the database.
        
        Keyword arguments:
        sql_query -- Query to be executed
        params -- Parameters to be passed to the query in where clauses to avoid SQL injection
        fetch -- Type of fetch operation: 'all', 'one' or 'none'
        transactional: Set to True if writing to the database, False for read operations.
        Return: Query results based on fetch type.
        """
        
        query = text(sql_query)
        
        if transactional:
            async with self.engine.begin() as conn:
                return await self._run(conn, query, params, fetch)
        else:
            async with self.engine.connect() as conn:
                return await self._run(conn, query, params, fetch)
    
    async def stream(
        self,
        sql_query: str,
        params: Optional[Union[Dict[str, Any], Sequence[Dict[str, Any]]]] = None,
        fetch: Literal["all", "one", "none"] = "all",
    ) -> AsyncConnection:
        """Streams results of a SQL query.
        
        Keyword arguments:
        sql_query -- Query to be executed
        params -- Parameters to be passed to the query in where clauses to avoid SQL injection
        fetch -- Type of fetch operation: 'all', 'one' or 'none'
        Return: Executor for streaming results.
        """
        
        query = text(sql_query)
        
        async with self.engine.connect() as conn:
            async for row in self._run(conn, query, params, fetch, stream=True):
                yield dict(row._mapping)
                
    async def _run(
        self,
        conn: AsyncConnection,
        query: str,
        params: Optional[Union[Dict[str, Any], Sequence[Dict[str, Any]]]] = None,
        fetch: Literal["all", "one", "none"] = "all",
        stream: bool = False
    ) -> Union[None, Sequence[Dict[str, Any]], Dict[str, Any]]:
        """Executes the query with the given connection.
        
        Keyword arguments:
        conn -- Database connection to use
        query -- SQL query to be executed
        params -- Parameters to be passed to the query in where clauses to avoid SQL injection
        fetch -- Type of fetch operation: 'all', 'one' or 'none'
        Return: Query results based on fetch and stream type.
        """
        
        if stream:
            result = await conn.stream(query, params or {})
            return result
        
        result = await conn.execute(query, params or {})
        
        if fetch == "one":
            row: Optional[Row] = result.fetchone()
            return dict(row._mapping) if row else {}
        elif fetch == "all":
            rows: Sequence[Row] = result.fetchall()
            return [dict(row._mapping) for row in rows]
        
        return None

@lru_cache
def get_db_manager(db_url: str) -> DBManager:
    """Returns a singleton instance of DBManager."""
    return DBManager(db_url)