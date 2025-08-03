from datetime import date

from app.features.dashboard.mess.types import QRScanLog, QRScanLogInput
from app.features.dashboard.mess.services import add_qr_scan_log_service
from app.features.shared.services import (
    get_table_data,
    get_table_row
)


async def get_qr_scan_logs_resolver(pg_id: str) -> list[QRScanLog]:
    res: list[QRScanLog] = []
    async for row in get_table_data(pg_id, "mess", "daily_scans"):
        if not row:
            raise Exception("No match found")
        res.append(QRScanLog(**row))

    return res


async def get_qr_scan_log_resolver(
        pg_id: str,
        tenant_id: str | None = None,
        meal_type: str | None = None,
        curr_date: date | None = None
) -> QRScanLog:
    filters = {}
    if tenant_id:
        filters["tenant_id"] = tenant_id
    if meal_type:
        filters["meal_type"] = meal_type
    if curr_date:
        filters["curr_date"] = curr_date

    result = await get_table_row(
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