from datetime import date
from strawberry import type, mutation
from strawberry.types import Info
from graphql import GraphQLError

from app.logger import AppLogger
from app.features.dashboard.mess.utils import trigger_dashboard_workers
from app.features.dashboard.mess.types import QRScanLog, QRScanLogInput, GetQRScanLog
from app.features.users.tenant.types import GetTenant
from app.features.users.tenant.resolver import get_tenant_by_pg_resolver
from app.features.dashboard.mess.resolver import (
    get_qr_scan_log_resolver,
    add_qr_scan_log_resolver
)

logger = AppLogger().get_logger()

@type
class QRScanMutation:
    @mutation
    async def add_qr_scan_log(
        self,
        data: QRScanLogInput,
        info: Info
    ) -> QRScanLog:

        pg_id = info.context["pg_id"]
        try:
            tenant = await get_tenant_by_pg_resolver(
                data=GetTenant(id=data.tenant_id),
                pg_id=pg_id
            )
            if not tenant:
                raise Exception('Tenant not registered in PG')

            tenant_has_scanned = await get_qr_scan_log_resolver(
                pg_id=pg_id,
                data=GetQRScanLog(
                    tenant_id=data.tenant_id,
                    meal_type=data.meal_type,
                    curr_date=date.today()
                )
            )
            if tenant_has_scanned:
                raise Exception('Tenant has already scanned')

            res = await add_qr_scan_log_resolver(data=data, pg_id=pg_id)

            await trigger_dashboard_workers(pg_id=pg_id, meal_type=data.meal_type)

            return res
        except Exception as e:
            logger.error(f"Error adding meal activity: {e}")
            raise GraphQLError(str(e))