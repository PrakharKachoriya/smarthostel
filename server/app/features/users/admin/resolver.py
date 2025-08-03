from app.logger import AppLogger
from app.features.users.admin.types import Pg, PgInput
from app.features.users.admin.services import add_pg_service
from app.features.shared.services import (
    delete_table_row,
    get_table_row,
    get_table_data
)


logger = AppLogger().get_logger()

async def get_pgs_resolver(pg_id: str) -> list[Pg]:
    res: list[Pg] = []
    async for row in get_table_data(pg_id, "core", "pg"):
        if not row:
            raise Exception("No match found")
        res.append(Pg(**row))

    return res


async def get_pg_resolver(pg_id: str) -> Pg:
    result = await get_table_row(
        pg_id, "core", "pg",
        and_filters={
            "id": pg_id
        }
    )
    if not result:
        raise Exception("Pg does not exist")

    return Pg(**result)


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
