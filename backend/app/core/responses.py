from typing import Any, Optional, Dict


def success(
    data: Any,
    message: str = "success",
    meta: Optional[Dict] = None,
) -> Dict:
    """
    Standardized success response format.
    {
        "success": true,
        "message": "success",
        "data": {...},
        "meta": {...}
    }
    """
    return {
        "success": True,
        "message": message,
        "data": data,
        "meta": meta or {},
    }


def error(
    message: str = "error",
    code: int = 400,
    error_code: Optional[str] = None,
) -> Dict:
    """
    Standardized error response format.
    {
        "success": false,
        "message": "...",
        "code": 400,
        "error_code": "ERROR_CODE"
    }
    """
    return {
        "success": False,
        "message": message,
        "code": code,
        "error_code": error_code or "UNKNOWN_ERROR",
    }


def paginated(
    items: Any,
    page: int,
    limit: int,
    total: int,
    message: str = "success",
) -> Dict:
    """
    Standardized paginated response.
    {
        "success": true,
        "message": "success",
        "data": {
            "items": [...],
            "page": 1,
            "limit": 20,
            "total": 100,
            "total_pages": 5
        },
        "meta": {...}
    }
    """
    total_pages = (total + limit - 1) // limit if limit > 0 else 0
    return success(
        {
            "items": items,
            "page": page,
            "limit": limit,
            "total": total,
            "total_pages": total_pages,
        },
        message=message,
        meta={
            "page_count": len(items),
            "has_next": page < total_pages if total_pages > 0 else False,
        },
    )

