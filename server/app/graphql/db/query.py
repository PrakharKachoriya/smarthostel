import strawberry
from strawberry.types import Info

from app.graphql.db.types import Tenant, MealActivity
from app.business.definitions.read import (
    get_table_data,
    get_tenants as get_tenants_data,
    get_mealactivity as get_mealactivity_data
)


@strawberry.type
class Query:
    @strawberry.field
    async def get_tenants(self, info: Info) -> list[Tenant]:
        return [Tenant(**row) async for row in get_table_data("core", "tenant")]
    
    @strawberry.field
    async def get_mealactivity(self, info: Info) -> list[MealActivity]:
        return [MealActivity(**row) async for row in get_table_data("analytics", "meal_activity_fact")]