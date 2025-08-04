import strawberry

from app.features.shared.mutations import SharedMutation
from app.features.users.tenant.mutations import TenantMutation
from app.features.users.admin.mutations import PgMutation
from app.features.users.staff.mutations import StaffMutation
from app.features.dashboard.mess.mutations import QRScanMutation


@strawberry.type
class Mutation(
    TenantMutation,
    PgMutation,
    StaffMutation,
    QRScanMutation,
    SharedMutation
):
    pass