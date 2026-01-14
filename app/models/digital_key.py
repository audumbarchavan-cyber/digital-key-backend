from sqlalchemy import Integer, String, Column
from app.db.database import Base

class DigitalKey(Base):
    __tablename__ = "digital_keys"

    id = Column(Integer, primary_key=True, index=True)
    key_name = Column(String, unique=True, index=True, nullable=False)
    key_value = Column(String, unique=True, index=True, nullable=False)
    owner = Column(String, index=True, nullable=False)