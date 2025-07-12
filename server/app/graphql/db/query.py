import strawberry
from strawberry.types import Info

from app.graphql.db.types import Tenant, MealActivity


@strawberry.type
class Query:
    @strawberry.field
    async def get_tenants(self, info: Info) -> list[Tenant]:
        pass
    
    @strawberry.field
    async def get_mealactivity(self, info: Info) -> list[MealActivity]:
        pass