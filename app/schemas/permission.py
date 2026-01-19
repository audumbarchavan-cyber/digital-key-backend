from pydantic import BaseModel
from datetime import datetime
from enum import Enum


class MachineType(str, Enum):
    SERVER = "server"
    WORKSTATION = "workstation"
    IOT_DEVICE = "iot_device"
    DATABASE = "database"
    STORAGE = "storage"
    OTHER = "other"


class MachineCreate(BaseModel):
    machine_name: str
    machine_type: MachineType
    ip_address: str | None = None
    description: str | None = None


class MachineUpdate(BaseModel):
    machine_name: str | None = None
    machine_type: MachineType | None = None
    ip_address: str | None = None
    description: str | None = None
    is_active: int | None = None


class MachineResponse(BaseModel):
    id: int
    machine_name: str
    machine_type: MachineType
    ip_address: str | None
    description: str | None
    is_active: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
