import strawberry
from strawberry.types import Info
from app.graphql.db.types import Tenant, MealActivity, TenantInput, MealActivityInput
from app.business.definitions.write import add_new_tenant, add_new_mealactivity
from app.business.ddl.methods import create_schema_if_not_exists, create_table_if_not_exists


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_tenant(self, data: TenantInput, info: Info) -> list[Tenant]:
        print(**data)
        # add_new_tenant(**data)
        
    
    @strawberry.mutation
    async def add_mealactivity(self, data: MealActivityInput, info: Info) -> list[MealActivity]:
        print(**data)
        # add_new_mealactivity(**data)
    
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