from app.logger import AppLogger
from app.features.users.admin.types import Pg, PgInput, GetPg
from app.features.users.admin.services import add_pg_service
from app.features.shared.services import (
    delete_table_row,
    get_table_data_ext,
    get_table_row_ext
)


logger = AppLogger().get_logger()

async def get_pgs_resolver() -> list[Pg]:
    res: list[Pg] = []
    async for row in get_table_data_ext("core", "pg"):
        if not row:
            raise Exception("No match found")
        res.append(Pg(**row))

    return res


async def get_pg_resolver(data: GetPg) -> Pg:
    if not (data.id or data.email):
        raise Exception("Either ID or Email required")
    filters = {}
    if data.email:
        filters["email"] = data.email
    else:
        filters["id"] = data.id

    result = await get_table_row_ext(
        "core", "pg",
        and_filters=filters
    )
    if not result:
        raise Exception("Pg does not exist")

    return Pg(**result)


async def login_pg_resolver(
    data: GetPg
) -> Pg:
    res = await get_pg_resolver(data=data)
    if res.password != data.password:
        raise Exception("Incorrect password, Try again")

    return res


async def add_pg_resolver(data: PgInput) -> Pg:
    result = await add_pg_service(data=data.to_pydantic())
    if not result:
        raise Exception("Could not add Pg")

    return Pg(**result)


async def delete_pg_resolver(pg_id: str) -> Pg:
    result = await delete_table_row(
        str(pg_id), "core", "pg",
        and_filters={
            "id": pg_id
        }
    )
    if not result:
        raise Exception("Pg could not be deleted: does not exist")

    return Pg(**result)
