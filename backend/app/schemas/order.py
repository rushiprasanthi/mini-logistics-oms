from typing import List, Optional

from pydantic import BaseModel, validator


class OrderBase(BaseModel):
    external_id: str

    @validator("external_id")
    def validate_external_id(cls, value):
        value = value.strip()

        if len(value) < 3:
            raise ValueError("external_id_too_short")

        return value


class OrderCreate(OrderBase):
    customer_id: Optional[int]


class OrderRead(OrderBase):
    id: int
    status: str
    customer_id: Optional[int]

    class Config:
        orm_mode = True


class PaginatedOrders(BaseModel):
    total: int
    page: int
    limit: int
    items: List[OrderRead]

    class Config:
        orm_mode = True
