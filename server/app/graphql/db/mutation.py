import strawberry
from strawberry.types import Info

from app.graphql.db.types import Tenant, MealActivity, TenantInput, MealActivityInput
from app.business.definitions.write import add_new_tenant, add_new_mealactivity


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