from strawberry import type, field
from strawberry.types import Info
from graphql import GraphQLError

from app.logger import AppLogger
from app.features.users.tenant.types import Tenant
from app.features.users.tenant.resolver import (
    get_tenant_resolver,
    get_tenants_resolver
)

logger = AppLogger().get_logger()

@type
class TenantQuery:
    @field
    async def get_tenant(self, tenant_id: str, info: Info) -> Tenant:
        pg_id = info.context["pg_id"]
        try:
            res = await get_tenant_resolver(tenant_id, pg_id=pg_id)
            return res
        except Exception as e:
            logger.error(e)
            raise GraphQLError(message=str(e))

    @field
    async def get_tenants(self, info: Info) -> list[Tenant]:
        pg_id = info.context["pg_id"]
        try:
            res = await get_tenants_resolver(pg_id=pg_id)
            return res
        except Exception as e:
            raise GraphQLError(f"Failed to fetch tenants: {str(e)}")