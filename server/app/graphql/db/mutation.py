import strawberry
from strawberry.types import Info
from app.graphql.db.types import TenantInput, MealActivityInput
from app.business.definitions.write import add_new_tenant, add_new_mealactivity
from app.business.ddl.methods import create_schema_if_not_exists, create_table_if_not_exists
from app.logger import AppLogger
from app.core.trigger_queue import get_trigger_queue

logger = AppLogger().get_logger()

trigger_queue = get_trigger_queue()

@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_tenant(self, data: TenantInput, info: Info) -> None:
        # print(data.__dict__)
        try:
            await add_new_tenant(**data.__dict__)
            
        except Exception as e:
            logger.error(e)
    
    @strawberry.mutation
    async def add_mealactivity(self, data: MealActivityInput, info: Info) -> None:
        # print(data.__dict__)
        try:
            await add_new_mealactivity(**data.__dict__)
            
            trigger_payload = {
                "action": "meal_activity_added",
                "pg_key": "slh",
                "meal_type": data.meal_type
            }
            
            await trigger_queue.enqueue(trigger_payload)
        except Exception as e:
            logger.error(f"Error adding meal activity: {e}")
            return None
    
    @strawberry.mutation
    async def create_schema(self, schema_name: str, info: Info) -> None:
        """Create a new schema in the database."""
        
        try:
            await create_schema_if_not_exists(schema_name)
        except Exception as e:
            print(f"Error creating schema {schema_name}: {e}")
            return None

    @strawberry.mutation
    async def create_table(self, schema_name: str, table_name: str, columns: list[str], info: Info) -> None:
        """Create a new table in the specified schema."""
        
        try:
            await create_table_if_not_exists(schema_name, table_name, columns)
        except Exception as e:
            print(f"Error creating table {schema_name}.{table_name}: {e}")
            return None