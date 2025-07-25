from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection
from sqlalchemy.engine import Row
from sqlalchemy import text
from sqlalchemy.sql.elements import TextClause
from typing import Optional, Union, Dict, Any, Sequence, Literal, AsyncGenerator
from functools import lru_cache

class DBManager:
    def __init__(self, db_url: str) -> "DBManager":
        self.db_url = db_url
        self._engine = None
    
    @property
    def engine(self) -> AsyncEngine:
        if self._engine is None:
            self._engine = create_async_engine(
                self.db_url,
                echo=True,
                pool_size=20,
                max_overflow=10,
                pool_timeout=30,
                pool_recycle=1800
            )
        return self._engine
    
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
    ) -> AsyncGenerator[Any, Any]:
        """Streams results of a SQL query.
        
        Keyword arguments:
        sql_query -- Query to be executed
        params -- Parameters to be passed to the query in where clauses to avoid SQL injection
        fetch -- Type of fetch operation: 'all', 'one' or 'none'
        Return: Executor for streaming results.
        """
        
        query = text(sql_query)
        
        async with self.engine.connect() as conn:
            result = await conn.execute(query, params or {})
            async for row in result:
                yield dict(row._mapping)
    
    async def run_ddl(
        self,
        sql_query: str,
    ) -> AsyncGenerator[Any, Any]:
        
        query = text(sql_query)
        
        async with self.engine.begin() as conn:
            result = await conn.execute(query, {})
            return None
    
    async def _run(
        self,
        conn: AsyncConnection,
        query: TextClause,
        params: Optional[Union[Dict[str, Any], Sequence[Dict[str, Any]]]] = None,
        fetch: Literal["all", "one", "none"] = "all",
    ) -> Union[None, Sequence[Dict[str, Any]], Dict[str, Any]]:
        """Executes the query with the given connection.
        
        Keyword arguments:
        conn -- Database connection to use
        query -- SQL query to be executed
        params -- Parameters to be passed to the query in where clauses to avoid SQL injection
        fetch -- Type of fetch operation: 'all', 'one' or 'none'
        Return: Query results based on fetch and stream type.
        """
        
        result = await conn.execute(query, params or {})
        print(result)
        
        if fetch == "one":
            row: Optional[Row] = result.fetchone()
            return dict(row._mapping) if row else {}
        elif fetch == "all":
            rows: Sequence[Row] = result.fetchall()
            for row in rows:
                print(row, row._mapping)
            return [dict(row._mapping) for row in rows]
        
        return None

@lru_cache
def get_db_manager(db_url: str) -> DBManager:
    """Returns a singleton instance of DBManager."""
    return DBManager(db_url)
