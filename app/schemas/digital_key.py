from pydantic import BaseModel

class DigitalKeyCreate(BaseModel):
    key_name: str
    key_value: str
    owner: str

class DigitalKeyResponse(DigitalKeyCreate):
    id: int

    class Config:
        orm_mode = True