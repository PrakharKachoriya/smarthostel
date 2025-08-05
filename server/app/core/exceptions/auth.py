from .base import BaseAppException

class UnauthorizedException(BaseAppException):
    def __init__(self):
        super().__init__(
            "Unauthorized access",
            status="UNAUTHORIZED",
            code=403
        )
