from sqlalchemy.orm import Session
from app.models.digital_key import DigitalKey
from app.schemas.digital_key import DigitalKeyCreate

def create_digital_key(db: Session, digital_key: DigitalKeyCreate) -> DigitalKey:
    db_digital_key = DigitalKey(
        key_name=digital_key.key_name,
        key_value=digital_key.key_value,
        owner=digital_key.owner
    )
    db.add(db_digital_key)
    db.commit()
    db.refresh(db_digital_key)
    return db_digital_key

def get_digital_key_by_id(db: Session, key_id: int) -> DigitalKey | None:
    return db.query(DigitalKey).filter(DigitalKey.id == key_id).first()

def get_all_digital_keys(db: Session) -> list[DigitalKey]:
    return db.query(DigitalKey).all()

def update_digital_key(db: Session, key_id: int, digital_key: DigitalKeyCreate) -> DigitalKey | None:
    db_digital_key = db.query(DigitalKey).filter(DigitalKey.id == key_id).first()
    if db_digital_key:
        db_digital_key.key_name = digital_key.key_name
        db_digital_key.key_value = digital_key.key_value
        db_digital_key.owner = digital_key.owner
        db.commit()
        db.refresh(db_digital_key)
        return db_digital_key
    return None

def delete_digital_key(db: Session, key_id: int) -> bool:
    digital_key = db.query(DigitalKey).filter(DigitalKey.id == key_id).first()
    if digital_key:
        db.delete(digital_key)
        db.commit()
        return True
    return False