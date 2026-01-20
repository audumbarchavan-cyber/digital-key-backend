from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class PermissionLevel(str, Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


class UserMachinePermissionCreate(BaseModel):
    user_id: int
    machine_id: int
    digital_key_id: int
    permission_level: PermissionLevel = PermissionLevel.READ


class UserMachinePermissionUpdate(BaseModel):
    permission_level: PermissionLevel | None = None
    is_active: bool | None = None


class UserMachinePermissionResponse(BaseModel):
    id: int
    user_id: int
    machine_id: int
    digital_key_id: int
    permission_level: PermissionLevel
    is_active: bool
    created_at: datetime
    updated_at: datetime
    revoked_at: datetime | None

    class Config:
        from_attributes = True


class UserAccessResponse(BaseModel):
    """Response showing user with their machine access permissions"""
    user_id: int
    username: str
    machine_id: int
    machine_name: str
    permission_level: PermissionLevel
    is_active: bool
    created_at: datetime
