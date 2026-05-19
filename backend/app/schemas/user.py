from typing import Optional

from pydantic import BaseModel, EmailStr, validator


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str

    @validator("password")
    def validate_password(cls, value):
        if len(value) < 6:
            raise ValueError("password_too_short")

        return value


class UserRead(UserBase):
    id: int
    is_active: bool
    role: str

    class Config:
        orm_mode = True
        fields = {
            'hashed_password': {'exclude': True},
        }
