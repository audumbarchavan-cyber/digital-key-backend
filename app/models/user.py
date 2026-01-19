from sqlalchemy import Integer, String, Column, DateTime, Enum as SQLEnum
from datetime import datetime
import enum
from app.db.database import Base


class UserType(str, enum.Enum):
    ADMIN = "admin"
    USER = "user"
    OPERATOR = "operator"
    VIEWER = "viewer"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    user_type = Column(SQLEnum(UserType), default=UserType.USER, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
