from sqlalchemy import Integer, String, Column, DateTime, Enum as SQLEnum
from datetime import datetime
import enum
from app.db.database import Base


class MachineType(str, enum.Enum):
    SERVER = "server"
    WORKSTATION = "workstation"
    IOT_DEVICE = "iot_device"
    DATABASE = "database"
    STORAGE = "storage"
    OTHER = "other"


class Machine(Base):
    __tablename__ = "machines"

    id = Column(Integer, primary_key=True, index=True)
    machine_name = Column(String, unique=True, index=True, nullable=False)
    machine_type = Column(SQLEnum(MachineType), nullable=False)
    ip_address = Column(String, nullable=True)
    description = Column(String, nullable=True)
    is_active = Column(Integer, default=1, nullable=False)  # 1 for active, 0 for inactive
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
