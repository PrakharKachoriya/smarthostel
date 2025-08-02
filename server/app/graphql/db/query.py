import strawberry
from strawberry.types import Info

from app.graphql.db.types import Tenant, QRScanLog
from app.business.definitions.read import (
    get_table_data
)


@strawberry.type
class Query:
    @strawberry.field
    async def get_tenants(self, info: Info) -> list[Tenant]:
        return [Tenant(**row) async for row in get_table_data("core", "tenant")]
    
    @strawberry.field
    async def get_qr_scan_logs(self, info: Info) -> list[QRScanLog]:
        return [QRScanLog(**row) async for row in get_table_data("mess", "daily_scans")]