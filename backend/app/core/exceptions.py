from fastapi import HTTPException
from typing import Optional, Any


class AppError(HTTPException):
    """Base application error with standardized format."""
    def __init__(self, status_code: int = 400, detail: str = "error", code: Optional[str] = None):
        self.code = code or "APP_ERROR"
        super().__init__(status_code=status_code, detail=detail)


class ValidationError(AppError):
    """Raised when input validation fails."""
    def __init__(self, detail: str = "validation failed", code: str = "VALIDATION_ERROR"):
        super().__init__(status_code=422, detail=detail, code=code)


class UnauthorizedError(AppError):
    """Raised when authentication fails."""
    def __init__(self, detail: str = "unauthorized", code: str = "UNAUTHORIZED"):
        super().__init__(status_code=401, detail=detail, code=code)


class ForbiddenError(AppError):
    """Raised when user lacks required permissions."""
    def __init__(self, detail: str = "forbidden", code: str = "FORBIDDEN"):
        super().__init__(status_code=403, detail=detail, code=code)


class NotFoundError(AppError):
    """Raised when resource not found."""
    def __init__(self, detail: str = "not found", code: str = "NOT_FOUND"):
        super().__init__(status_code=404, detail=detail, code=code)


class ConflictError(AppError):
    """Raised when resource already exists (duplicate key, etc)."""
    def __init__(self, detail: str = "resource already exists", code: str = "CONFLICT"):
        super().__init__(status_code=409, detail=detail, code=code)


class InvalidTransitionError(AppError):
    """Raised when FSM transition is invalid."""
    def __init__(self, from_status: str, to_status: str, code: str = "INVALID_TRANSITION"):
        detail = f"cannot transition from {from_status} to {to_status}"
        super().__init__(status_code=400, detail=detail, code=code)


class DuplicateError(AppError):
    """Raised when unique constraint would be violated."""
    def __init__(self, detail: str = "duplicate resource", code: str = "DUPLICATE"):
        super().__init__(status_code=409, detail=detail, code=code)

