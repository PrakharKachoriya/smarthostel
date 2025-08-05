from .base import BaseAppException

# --------------------------------------------------
# 42X series is for tenants
# --------------------------------------------------

# TENANT
class TenantDoesNotExistException(BaseAppException):
    def __init__(self):
        super().__init__(
            "Tenant does not exist",
            status="TENANT_NOT_FOUND",
            code=420
        )

class TenantAlreadyExistsException(BaseAppException):
    def __init__(self):
        super().__init__(
            "Tenant already exists",
            status="TENANT_EXISTS",
            code=421
        )

class TenantAlreadyScannedException(BaseAppException):
    def __init__(self):
        super().__init__(
            "Tenant has already been scanned",
            status="TENANT_ALREADY_SCANNED",
            code=422
        )


# --------------------------------------------------
# 43X series is for staff
# --------------------------------------------------

# STAFF
class StaffDoesNotExistException(BaseAppException):
    def __init__(self):
        super().__init__(
            "Staff does not exist",
            status="STAFF_NOT_FOUND",
            code=430
        )

class StaffAlreadyExistsException(BaseAppException):
    def __init__(self):
        super().__init__(
            "Staff already exists",
            status="STAFF_EXISTS",
            code=431
        )

# --------------------------------------------------
# 44X series is for admin
# --------------------------------------------------

# PG
class PgDoesNotExistException(BaseAppException):
    def __init__(self):
        super().__init__(
            "PG does not exist",
            status="PG_NOT_FOUND",
            code=440
        )

class PgAlreadyExistsException(BaseAppException):
    def __init__(self):
        super().__init__(
            "PG already exists",
            status="PG_EXISTS",
            code=441
        )