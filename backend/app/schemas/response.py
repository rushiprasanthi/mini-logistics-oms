from typing import Generic, Optional, TypeVar, Any

from pydantic import BaseModel
from pydantic.generics import GenericModel


T = TypeVar("T")


class SuccessResponse(GenericModel, Generic[T]):
    success: bool = True
    message: str = "success"
    data: Optional[T] = None
    meta: Optional[Any] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    code: int
    data: Optional[Any] = None
