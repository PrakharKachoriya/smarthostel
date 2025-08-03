from app.logger import AppLogger
from app.features.users.tenant.types import Tenant, TenantInput
from app.features.users.tenant.services import add_tenant_service
from app.features.shared.services import (
    delete_table_row,
    get_table_row,
    get_table_data
)


logger = AppLogger().get_logger()

async def get_tenants_resolver(pg_id: str) -> list[Tenant]:
    res: list[Tenant] = []
    async for row in get_table_data(pg_id, "core", "tenant"):
        if not row:
            raise Exception("No match found")
        res.append(Tenant(**row))

    return res


async def get_tenant_resolver(tenant_id: str, pg_id: str) -> Tenant:
    result = await get_table_row(
        pg_id, "core", "tenant",
        and_filters={
            "id": tenant_id
        }
    )
    if not result:
        raise Exception("Tenant does not exist")

    return Tenant(**result)


async def add_tenant_resolver(data: TenantInput, pg_id: str) -> Tenant:
    # logger.info(f"Adding tenant to PG with ID: {pg_id}")
    result = await add_tenant_service(data=data.to_pydantic(), pg_id=str(pg_id))
    if not result:
        raise Exception("Could not add tenant")

    return Tenant(**result)


async def delete_tenant_resolver(tenant_id: str, pg_id: str) -> Tenant:
    result = await delete_table_row(
        str(pg_id), "core", "tenant",
        and_filters={
            "id": tenant_id
        }
    )
    if not result:
        raise Exception("Tenant could not be deleted: does not exist")

    return Tenant(**result)
