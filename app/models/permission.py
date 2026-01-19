from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, Enum as SQLEnum, Boolean
from datetime import datetime
import enum
from app.db.database import Base


class PermissionLevel(str, enum.Enum):
    READ = "read"
    WRITE = "write"
    EXECUTE = "execute"
    ADMIN = "admin"


class UserMachinePermission(Base):
    __tablename__ = "user_machine_permissions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    machine_id = Column(Integer, ForeignKey("machines.id"), nullable=False, index=True)
    digital_key_id = Column(Integer, ForeignKey("digital_keys.id"), nullable=False, index=True)
    permission_level = Column(SQLEnum(PermissionLevel), default=PermissionLevel.READ, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    revoked_at = Column(DateTime, nullable=True)
