from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class UserType(str, Enum):
    ADMIN = "admin"
    USER = "user"
    OPERATOR = "operator"
    VIEWER = "viewer"
    OWNER = "owner"


class UserCreate(BaseModel):
    username: str
    user_type: UserType = UserType.USER
    email: str


class UserUpdate(BaseModel):
    username: str | None = None
    user_type: UserType | None = None
    email: str | None = None


class UserResponse(BaseModel):
    id: int
    username: str
    user_type: UserType
    email: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
