from strawberry import type, field
from strawberry.types import Info
from graphql import GraphQLError

from app.features.dashboard.mess.types import GetQRScanLog, QRScanLog
from app.features.dashboard.mess.resolver import get_qr_scan_log_resolver


@type
class QRScanQuery:
    @field
    async def get_qr_scan_log(
        self,
        data: GetQRScanLog,
        info: Info
    ) -> QRScanLog:
        pg_ig = info.context["pg_id"]
        try:
            res = await get_qr_scan_log_resolver(
                pg_id=pg_ig,
                data=data
            )
            return res
        except Exception as e:
            raise GraphQLError(str(e))