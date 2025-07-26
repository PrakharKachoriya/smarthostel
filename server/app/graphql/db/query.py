import strawberry
from strawberry.types import Info

from app.graphql.db.types import Tenant, MealActivity
from app.business.definitions.read import get_tenants as get_tenants_data, get_mealactivity as get_mealactivity_data


@strawberry.type
class Query:
    @strawberry.field
    async def get_tenants(self, info: Info) -> list[Tenant]:
        return [Tenant(**row) async for row in get_tenants_data()]
    
    @strawberry.field
    async def get_mealactivity(self, info: Info) -> list[MealActivity]:
        return [MealActivity(**row) async for row in get_mealactivity_data()]