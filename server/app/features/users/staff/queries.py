from strawberry import type, field
from strawberry.types import Info
from graphql import GraphQLError

from app.logger import AppLogger
from app.features.users.staff.types import Staff, GetStaff
from app.features.users.staff.resolver import (
    get_staff_resolver_by_pg,
    get_staffs_resolver,
    login_staff_resolver
)

logger = AppLogger().get_logger()

@type
class StaffQuery:
    @field
    async def get_staff(self, data: GetStaff, info: Info) -> Staff:
        pg_id = info.context["pg_id"]
        try:
            res = await get_staff_resolver_by_pg(data=data, pg_id=pg_id)
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

    @field
    async def login_staff(self, data: GetStaff):
        try:
            res = await login_staff_resolver(data=data)
            return res
        except Exception as e:
            raise GraphQLError(f"Failed to fetch tenants: {str(e)}")