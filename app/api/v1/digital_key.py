from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.models.digital_key import Base
from app.schemas.digital_key import DigitalKeyCreate, DigitalKeyResponse
from app.services import digital_key_service
from app.utils.cloud import upload_to_cloud

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/digital-keys", tags=["Digital Keys"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=DigitalKeyResponse)
def create_digital_key(digital_key: DigitalKeyCreate, db: Session = Depends(get_db)):
    db_digital_key = digital_key_service.create_digital_key(db, digital_key)
    upload_to_cloud(db_digital_key)
    return db_digital_key

@router.get("/{key_id}", response_model=DigitalKeyResponse)
def read_digital_key(key_id: int, db: Session = Depends(get_db)):
    db_digital_key = digital_key_service.get_digital_key_by_id(db, key_id)
    if db_digital_key is None:
        raise HTTPException(status_code=404, detail="Digital Key not found")
    return db_digital_key

@router.get("/", response_model=list[DigitalKeyResponse])
def read_all_digital_keys(db: Session = Depends(get_db)):
    return digital_key_service.get_all_digital_keys(db)

@router.put("/{key_id}", response_model=DigitalKeyResponse)
def update_digital_key(key_id: int, digital_key: DigitalKeyCreate, db: Session = Depends(get_db)):
    db_digital_key = digital_key_service.update_digital_key(db, key_id, digital_key)
    if db_digital_key is None:
        raise HTTPException(status_code=404, detail="Digital Key not found")
    return db_digital_key

@router.delete("/{key_id}", response_model=dict)
def delete_digital_key(key_id: int, db: Session = Depends(get_db)):
    success = digital_key_service.delete_digital_key(db, key_id)
    if not success:
        raise HTTPException(status_code=404, detail="Digital Key not found")
    return {"detail": "Digital Key deleted successfully"}