import strawberry
from strawberry.types import Info
from graphql import GraphQLError

from app.logger import AppLogger
from app.features.shared.services import (
    create_table_if_not_exists,
    create_schema_if_not_exists
)


logger = AppLogger().get_logger()

@strawberry.type
class SharedMutation:
    @strawberry.mutation
    async def create_schema(self, schema_name: str, info: Info) -> None:
        """Create a new schema in the database."""

        try:
            await create_schema_if_not_exists(schema_name)
        except Exception as e:
            logger.error(f"Error creating schema {schema_name}: {e}")
            raise GraphQLError(f"Error creating schema {schema_name}: {e}")


    @strawberry.mutation
    async def create_table(self, schema_name: str, table_name: str, columns: list[str], info: Info) -> None:
        """Create a new table in the specified schema."""

        try:
            # pg_id = info.context["pg_id"]
            # To be used for partitioning new table for pg id
            await create_table_if_not_exists(schema_name, table_name, columns)
        except Exception as e:
            logger.error(f"Error creating table {schema_name}.{table_name}: {e}")
            raise GraphQLError(f"Error creating table {schema_name}.{table_name}: {e}")