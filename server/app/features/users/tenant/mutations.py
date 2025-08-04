import strawberry
from strawberry.types import Info
from graphql import GraphQLError

from app.logger import AppLogger
from app.features.users.tenant.types import Tenant, TenantInput
from app.features.users.tenant.resolver import (
    add_tenant_resolver,
    delete_tenant_resolver
)


logger = AppLogger().get_logger()


@strawberry.type
class TenantMutation:
    @strawberry.mutation
    async def add_tenant(self, data: TenantInput, info: Info) -> Tenant:
        pg_id = info.context["pg_id"]
        try:
            res = await add_tenant_resolver(data=data, pg_id=pg_id)
            return res
        except Exception as e:
            logger.error(e)
            raise GraphQLError(str(e))

    @strawberry.mutation
    async def delete_tenant(self, tenant_id: str, info: Info) -> Tenant:
        pg_id = info.context["pg_id"]
        try:
            res = await delete_tenant_resolver(tenant_id=tenant_id, pg_id=pg_id)
            return res
        except Exception as e:
            logger.error(e)
            raise GraphQLError(str(e))