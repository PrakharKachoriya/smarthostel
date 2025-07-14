import strawberry
from strawberry.types import Info

from app.graphql.db.types import Tenant, MealActivity
from app.business.definitions.read import get_tenants, get_mealactivity


@strawberry.type
class Query:
    @strawberry.field
    async def get_tenants(self, info: Info) -> list[Tenant]:
        async for row in get_tenants():
            print(row)
        return []
    
    @strawberry.field
    async def get_mealactivity(self, info: Info) -> list[MealActivity]:
        async for row in get_mealactivity():
            print(row)
        return []