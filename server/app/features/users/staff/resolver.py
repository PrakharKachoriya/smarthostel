from app.logger import AppLogger
from app.features.users.staff.types import Staff, StaffInput, GetStaff
from app.features.users.staff.services import add_staff_service
from app.features.shared.services import (
    delete_table_row,
    get_table_row_ext,
    get_table_row_by_pg,
    get_table_data_by_pg
)


logger = AppLogger().get_logger()

async def get_staffs_resolver(pg_id: str) -> list[Staff]:
    res: list[Staff] = []
    async for row in get_table_data_by_pg(pg_id, "core", "staff"):
        if not row:
            raise Exception("No match found")
        res.append(Staff(**row))

    return res


async def get_staff_resolver_by_pg(data: GetStaff, pg_id: str) -> Staff:
    if not (data.id or data.email or data.phone_number):
        raise Exception("Either Id or email or number required")
    filters = {}
    if data.phone_number:
        filters["phone_number"] = data.phone_number
    elif data.email:
        filters["email"] = data.email
    elif data.id:
        filters["id"] = data.id

    result = await get_table_row_by_pg(
        pg_id, "core", "staff",
        and_filters=filters
    )
    if not result:
        raise Exception("Tenant does not exist")

    return Staff(**result)


async def get_staff_resolver(data: GetStaff) -> Staff:
    if not (data.id or data.email or data.phone_number):
        raise Exception("Either Id or email or number required")
    filters = {}
    if data.phone_number:
        filters["phone_number"] = data.phone_number
    elif data.email:
        filters["email"] = data.email
    elif data.id:
        filters["id"] = data.id

    result = await get_table_row_ext(
        "core", "staff",
        and_filters=filters
    )
    if not result:
        raise Exception("Tenant does not exist")

    return Staff(**result)


async def login_staff_resolver(
    data: GetStaff
) -> Staff:
    res = await get_staff_resolver(data=data)
    if res.password != data.password:
        raise Exception("Incorrect password, Try again")

    return res


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
