from strawberry import type

from app.features.users.tenant.mutations import TenantMutation
from app.features.users.admin.mutations import PgMutation
from app.features.users.staff.mutations import StaffMutation
from app.features.dashboard.mess.mutations import QRScanMutation


@type
class Mutation(
    TenantMutation,
    PgMutation,
    StaffMutation,
    QRScanMutation
):
    pass