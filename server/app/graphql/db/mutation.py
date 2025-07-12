import strawberry
from strawberry.types import Info

from app.graphql.db.types import Tenant, MealActivity, TenantInput, MealActivityInput


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def add_tenant(self, data: TenantInput, info: Info) -> list[Tenant]:
        pass
    
    @strawberry.mutation
    async def add_mealactivity(self, data: MealActivityInput, info: Info) -> list[MealActivity]:
        pass