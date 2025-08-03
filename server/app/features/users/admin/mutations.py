from strawberry import type, mutation
from strawberry.types import Info
from graphql import GraphQLError

from app.logger import AppLogger
from app.features.users.admin.types import Pg, PgInput
from app.features.users.admin.resolver import (
    add_pg_resolver,
    delete_pg_resolver
)


logger = AppLogger().get_logger()

@type
class PgMutation:
    @mutation
    async def add_pg(self, data: PgInput, info: Info) -> Pg:
        try:
            res = await add_pg_resolver(data=data)
            return res
        except Exception as e:
            logger.error(e)
            raise GraphQLError(str(e))

    @mutation
    async def delete_pg(self, info: Info) -> Pg:
        pg_id = info.context["pg_id"]
        try:
            res = await delete_pg_resolver(pg_id=pg_id)
            return res
        except Exception as e:
            logger.error(e)
            raise GraphQLError(str(e))