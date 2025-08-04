import strawberry
from strawberry.types import Info
from graphql import GraphQLError

from app.logger import AppLogger
from app.features.users.tenant.types import Tenant, GetTenant
from app.features.users.tenant.resolver import (
    get_tenant_by_pg_resolver,
    get_tenants_resolver,
    login_tenant_resolver
)

logger = AppLogger().get_logger()

@strawberry.type
class TenantQuery:
    @strawberry.field
    async def get_tenant(self, data: GetTenant, info: Info) -> Tenant:
        pg_id = info.context["pg_id"]
        try:
            res = await get_tenant_by_pg_resolver(data=data, pg_id=pg_id)
            return res
        except Exception as e:
            logger.error(e)
            # return Tenant(**{})
            raise GraphQLError(str(e))

    @strawberry.field
    async def get_tenants(self, info: Info) -> list[Tenant]:
        pg_id = info.context["pg_id"]
        try:
            res = await get_tenants_resolver(pg_id=pg_id)
            return res
        except Exception as e:
            # return [Tenant(**{})]
            raise GraphQLError(f"Failed to fetch tenants: {str(e)}")

    @strawberry.field
    async def login_tenant(self, data: GetTenant, info: Info) -> Tenant:
        try:
            res = await login_tenant_resolver(data=data)
            return res
        except Exception as e:
            # return Tenant(**{})
            raise GraphQLError(f"Failed to fetch tenants: {str(e)}")