from app.features.dashboard.mess.types import QRScanLog, QRScanLogInput, GetQRScanLog
from app.features.dashboard.mess.services import add_qr_scan_log_service
from app.features.shared.services import (
    get_table_data_by_pg,
    get_table_row_by_pg
)


async def get_qr_scan_logs_resolver(pg_id: str) -> list[QRScanLog]:
    res: list[QRScanLog] = []
    async for row in get_table_data_by_pg(pg_id, "mess", "daily_scans"):
        if not row:
            raise Exception("No match found")
        res.append(QRScanLog(**row))

    return res


async def get_qr_scan_log_resolver(
    pg_id: str,
    data: GetQRScanLog
) -> QRScanLog:
    if not (data.tenant_id or data.meal_type or data.curr_date):
        raise Exception("Either Tenant ID or Meal Type or Date required")
    filters = {}
    if data.tenant_id:
        filters["tenant_id"] = data.tenant_id
    if data.meal_type:
        filters["meal_type"] = data.meal_type
    if data.curr_date:
        filters["curr_date"] = data.curr_date

    result = await get_table_row_by_pg(
        pg_id, "mess", "daily_scans",
        and_filters=filters
    )
    if not result:
        raise Exception("Tenant does not exist")

    return QRScanLog(**result)


async def add_qr_scan_log_resolver(data: QRScanLogInput, pg_id: str) -> QRScanLog:
    res = await add_qr_scan_log_service(data=data.to_pydantic(), pg_id=pg_id)
    if not res:
        raise Exception("Could not add QR Scan Log")
    return QRScanLog(**res)