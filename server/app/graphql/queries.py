from strawberry import type

from app.features.users.tenant.queries import TenantQuery
from app.features.users.admin.queries import PgQuery
from app.features.users.staff.queries import StaffQuery
from app.features.dashboard.mess.queries import QRScanQuery


@type
class Query(
    TenantQuery,
    PgQuery,
    StaffQuery,
    QRScanQuery
):
    pass