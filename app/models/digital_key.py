from sqlalchemy import Integer, String, Column, ForeignKey, DateTime
from datetime import datetime
from app.db.database import Base

class DigitalKey(Base):
    __tablename__ = "digital_keys"

    id = Column(Integer, primary_key=True, index=True)
    key_name = Column(String, unique=True, index=True, nullable=False)
    key_value = Column(String, unique=True, index=True, nullable=False)
    owner = Column(String, index=True, nullable=False)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)