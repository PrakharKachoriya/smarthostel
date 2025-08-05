class BaseAppException(Exception):
    def __init__(self, message: str, status: str = "BAD_REQUEST", code: int = 400):
        self.message = message
        self.status = status
        self.code = code
        super().__init__(message, status, code)