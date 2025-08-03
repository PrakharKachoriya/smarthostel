from app.logger import AppLogger
from app.features.users.staff.types import Staff, StaffInput
from app.features.users.staff.services import add_staff_service
from app.features.shared.services import (
    delete_table_row,
    get_table_row,
    get_table_data
)


logger = AppLogger().get_logger()

async def get_staffs_resolver(pg_id: str) -> list[Staff]:
    res: list[Staff] = []
    async for row in get_table_data(pg_id, "core", "staff"):
        if not row:
            raise Exception("No match found")
        res.append(Staff(**row))

    return res


async def get_staff_resolver(tenant_id: str, pg_id: str) -> Staff:
    result = await get_table_row(
        pg_id, "core", "staff",
        and_filters={
            "id": tenant_id
        }
    )
    if not result:
        raise Exception("Tenant does not exist")

    return Staff(**result)


async def add_staff_resolver(data: StaffInput, pg_id: str) -> Staff:
    # logger.info(f"Adding tenant to PG with ID: {pg_id}")
    result = await add_staff_service(data=data.to_pydantic(), pg_id=str(pg_id))
    if not result:
        raise Exception("Could not add tenant")

    return Staff(**result)


async def delete_staff_resolver(tenant_id: str, pg_id: str) -> Staff:
    result = await delete_table_row(
        str(pg_id), "core", "staff",
        and_filters={
            "id": tenant_id
        }
    )
    if not result:
        raise Exception("Staff could not be deleted: does not exist")

    return Staff(**result)
