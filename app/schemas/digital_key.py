from pydantic import BaseModel
from datetime import datetime

class DigitalKeyCreate(BaseModel):
    key_name: str
    key_value: str
    owner: str
    machine_id: int

class DigitalKeyResponse(DigitalKeyCreate):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True