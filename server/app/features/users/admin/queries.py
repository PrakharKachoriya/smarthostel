from strawberry import type, field
from strawberry.types import Info
from graphql import GraphQLError

from app.logger import AppLogger
from app.features.users.admin.types import Pg
from app.features.users.admin.resolver import (
    get_pg_resolver,
    get_pgs_resolver
)

logger = AppLogger().get_logger()

@type
class PgQuery:
    @field
    async def get_pg(self, tenant_id: str, info: Info) -> Pg:
        pg_id = info.context["pg_id"]
        try:
            res = await get_pg_resolver(pg_id=pg_id)
            return res
        except Exception as e:
            logger.error(e)
            raise GraphQLError(message=str(e))

    # @field
    # async def get_pgs(self, info: Info) -> list[Pg]:
    #     pg_id = info.context["pg_id"]
    #     try:
    #         res = await get_pgs_resolver(pg_id=pg_id)
    #         return res
    #     except Exception as e:
    #         raise GraphQLError(f"Failed to fetch tenants: {str(e)}")