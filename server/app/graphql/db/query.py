from strawberry import type, field
from strawberry.types import Info

from app.graphql.db.types import Tenant, QRScanLog
from app.business.definitions.read import (
    get_table_data
)


@type
class Query:
    @field
    async def get_tenants(self, info: Info) -> list[Tenant]:
        pg_id = info.context["pg_id"]
        return [Tenant(**row) async for row in get_table_data(pg_id, "core", "tenant")]
    
    @field
    async def get_qr_scan_logs(self, info: Info) -> list[QRScanLog]:
        pg_id = info.context["pg_id"]
        return [QRScanLog(**row) async for row in get_table_data(pg_id, "mess", "daily_scans")]