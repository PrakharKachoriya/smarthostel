from base import BaseAppException

# --------------------------------------------------
# 41X series is for credentials and schema
# --------------------------------------------------

class PasswordMismatchException(BaseAppException):
    def __init__(self):
        super().__init__(
            "Password does not match",
            status="PASSWORD_MISMATCH",
            code=410
        )

class PasswordRequiredException(BaseAppException):
    def __init__(self):
        super().__init__(
            "Password is required",
            status="PASSWORD_REQUIRED",
            code=411
        )

class EmailOrIDRequiredException(BaseAppException):
    def __init__(self):
        super().__init__(
            "Email or ID is required",
            status="EMAIL_OR_ID_REQUIRED",
            code=412
        )

class SchemaMismatchException(BaseAppException):
    def __init__(self):
        super().__init__(
            "Schema mismatch",
            status="SCHEMA_MISMATCH",
            code=413
        )