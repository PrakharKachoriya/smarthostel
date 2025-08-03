from strawberry import type, field
from strawberry.types import Info
from graphql import GraphQLError

from app.logger import AppLogger
from app.features.users.admin.types import Pg, GetPg
from app.features.users.admin.resolver import (
    get_pg_resolver,
    login_pg_resolver,
    get_pgs_resolver
)

logger = AppLogger().get_logger()

@type
class PgQuery:
    @field
    async def get_pg(self, data: GetPg, info: Info) -> Pg:
        try:
            res = await get_pg_resolver(data=data)
            return res
        except Exception as e:
            logger.error(e)
            raise GraphQLError(message=str(e))

    @field
    async def login_pg(self, data: GetPg):
        try:
            res = await login_pg_resolver(data=data)
            return res
        except Exception as e:
            raise GraphQLError(f"Failed to fetch tenants: {str(e)}")

    # @field
    # async def get_pgs(self, info: Info) -> list[Pg]:
    #     try:
    #         res = await get_pgs_resolver()
    #         return res
    #     except Exception as e:
    #         raise GraphQLError(f"Failed to fetch tenants: {str(e)}")