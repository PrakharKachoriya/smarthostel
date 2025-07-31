from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, AsyncConnection
from sqlalchemy.engine import Row
from sqlalchemy import text
from sqlalchemy.sql.elements import TextClause
from sqlalchemy.pool import NullPool, QueuePool

from typing import Optional, Union, Dict, Any, Sequence, Literal, AsyncGenerator
from functools import lru_cache
from app.logger import AppLogger

logger = AppLogger().get_logger()

class DBManager:
    def __init__(self, db_url: str) -> "DBManager":
        logger.debug(f"Initializing DBManager with URL: {db_url}")
        self.db_url = db_url
        self._engine = None
        self._engine_v2 = None
    
    @property
    def engine(self) -> AsyncEngine:
        if self._engine is None:
            logger.debug("Creating new AsyncEngine instance")
            # Create the async engine with connection pooling
            # Pool size is set to 1000, with a maximum overflow of 200 connections
            # Pool timeout is set to 30 seconds, and pool recycle is set to 1800 seconds
            # This configuration is suitable for high concurrency applications
            self._engine = create_async_engine(
                self.db_url,
                echo=True,
                pool_size=100,
                max_overflow=40,
                pool_timeout=10,
                pool_recycle=1800,
            )
        return self._engine
    
    @property
    def engine_v2(self) -> AsyncEngine:
        """Returns a new AsyncEngine instance with NullPool."""
        logger.debug("Creating new AsyncEngine instance with NullPool")
        if not self._engine_v2:
            self._engine_v2 = create_async_engine(
                self.db_url,
                echo=True,
                poolclass=NullPool,
            )
        return self._engine_v2
    
    async def execute(
        self,
        sql_query: str,
        params: Optional[Union[Dict[str, Any], Sequence[Dict[str, Any]]]] = None,
        fetch: Literal["all", "one", "none"] = "all",
        transactional: bool = False,
        v2: bool = False
    ) -> Union[None, Sequence[Dict[str, Any]], Dict[str, Any]]:
        """Executes a SQL query against the database.
        
        Keyword arguments:
        sql_query -- Query to be executed
        params -- Parameters to be passed to the query in where clauses to avoid SQL injection
        fetch -- Type of fetch operation: 'all', 'one' or 'none'
        transactional: Set to True if writing to the database, False for read operations.
        Return: Query results based on fetch type.
        """
        
        logger.debug(f"Executing SQL query: {sql_query} with params: {params} and fetch type: {fetch}")
        query = text(sql_query)
        
        if v2:
            logger.debug("Using engine_v2 for query execution")
            async with self.engine_v2.connect() as conn:
                async with conn.begin():
                    return await self._run(conn, query, params, fetch)
        
        if transactional:
            logger.debug("Running query in a transactional context")
            async with self.engine.begin() as conn:
                return await self._run(conn, query, params, fetch)
        else:
            logger.debug("Running query in a non-transactional context")
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
        
        logger.debug(f"Streaming SQL query: {sql_query} with params: {params}")
        query = text(sql_query)
        
        async with self.engine.connect() as conn:
            logger.debug("Executing streaming query")
            result = await conn.execute(query, params or {})
            async for row in result:
                yield dict(row._mapping)
    
    async def run_ddl(
        self,
        sql_query: str,
        v2: bool = False
    ) -> AsyncGenerator[Any, Any]:
        
        logger.debug(f"Running DDL query: {sql_query}")
        query = text(sql_query)
        
        if v2:
            async with self.engine_v2.connect() as conn:
                logger.debug("Using engine_v2 for DDL query execution")
                async with conn.begin():
                    result = await conn.execute(query, {})
                    logger.debug("DDL query executed successfully")
                    return result.rowcount
        
        async with self.engine.begin() as conn:
            result = await conn.execute(query, {})
            logger.debug("DDL query executed successfully")
            return result.rowcount
    
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
