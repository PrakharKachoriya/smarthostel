import strawberry
from strawberry.types import Info
from graphql import GraphQLError

from app.logger import AppLogger
from app.features.users.staff.types import Staff, StaffInput
from app.features.users.staff.resolver import (
    add_staff_resolver,
    delete_staff_resolver
)


logger = AppLogger().get_logger()

@strawberry.type
class StaffMutation:
    @strawberry.mutation
    async def add_staff(self, data: StaffInput, info: Info) -> Staff:
        pg_id = info.context["pg_id"]
        try:
            res = await add_staff_resolver(data=data, pg_id=pg_id)
            return res
        except Exception as e:
            logger.error(e)
            raise GraphQLError(str(e))

    @strawberry.mutation
    async def delete_staff(self, tenant_id: str, info: Info) -> Staff:
        pg_id = info.context["pg_id"]
        try:
            res = await delete_staff_resolver(tenant_id=tenant_id, pg_id=pg_id)
            return res
        except Exception as e:
            logger.error(e)
            raise GraphQLError(str(e))