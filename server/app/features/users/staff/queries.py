from strawberry import type, field
from strawberry.types import Info
from graphql import GraphQLError

from app.logger import AppLogger
from app.features.users.staff.types import Staff
from app.features.users.staff.resolver import (
    get_staff_resolver,
    get_staffs_resolver
)

logger = AppLogger().get_logger()

@type
class StaffQuery:
    @field
    async def get_staff(self, tenant_id: str, info: Info) -> Staff:
        pg_id = info.context["pg_id"]
        try:
            res = await get_staff_resolver(tenant_id, pg_id=pg_id)
            return res
        except Exception as e:
            logger.error(e)
            raise GraphQLError(message=str(e))

    @field
    async def get_staffs(self, info: Info) -> list[Staff]:
        pg_id = info.context["pg_id"]
        try:
            res = await get_staffs_resolver(pg_id=pg_id)
            return res
        except Exception as e:
            raise GraphQLError(f"Failed to fetch tenants: {str(e)}")