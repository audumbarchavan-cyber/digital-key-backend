from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.models.digital_key import Base
from app.schemas.digital_key import DigitalKeyCreate, DigitalKeyResponse
from app.services import digital_key_service
from app.utils.cloud import upload_data_to_cloud, list_all_uploads, download_data_from_cloud

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
    """Create a new digital key and upload it to local cloud storage.
    
    Validates that the machine_id exists before creating the key.
    """
    result = digital_key_service.create_digital_key(db, digital_key)
    
    # Check if validation failed
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@router.get("/{key_id}", response_model=DigitalKeyResponse)
def read_digital_key(key_id: int, db: Session = Depends(get_db)):
    """Retrieve a digital key by ID."""
    db_digital_key = digital_key_service.get_digital_key_by_id(db, key_id)
    if db_digital_key is None:
        raise HTTPException(status_code=404, detail="Digital Key not found")
    return db_digital_key

@router.get("/", response_model=list[DigitalKeyResponse])
def read_all_digital_keys(db: Session = Depends(get_db)):
    """Retrieve all digital keys."""
    return digital_key_service.get_all_digital_keys(db)

@router.get("/machine/{machine_id}", response_model=list[DigitalKeyResponse])
def get_keys_by_machine(machine_id: int, db: Session = Depends(get_db)):
    """Retrieve all digital keys associated with a specific machine."""
    keys = digital_key_service.get_digital_keys_by_machine(db, machine_id)
    if not keys:
        raise HTTPException(status_code=404, detail="No digital keys found for this machine")
    return keys

@router.get("/name/{key_name}", response_model=DigitalKeyResponse)
def get_key_by_name(key_name: str, db: Session = Depends(get_db)):
    """Retrieve a digital key by its name."""
    key = digital_key_service.get_digital_key_by_name(db, key_name)
    if key is None:
        raise HTTPException(status_code=404, detail="Digital key not found")
    return key

@router.get("/owner/{owner}", response_model=list[DigitalKeyResponse])
def get_keys_by_owner(owner: str, db: Session = Depends(get_db)):
    """Retrieve all digital keys owned by a specific user."""
    keys = digital_key_service.get_digital_keys_by_owner(db, owner)
    if not keys:
        raise HTTPException(status_code=404, detail="No digital keys found for this owner")
    return keys

@router.put("/{key_id}", response_model=DigitalKeyResponse)
def update_digital_key(key_id: int, digital_key: DigitalKeyCreate, db: Session = Depends(get_db)):
    """Update a digital key and its cloud storage backup.
    
    Validates that the machine_id exists before updating the key.
    """
    result = digital_key_service.update_digital_key(db, key_id, digital_key)
    
    # Check if key not found
    if result is None:
        raise HTTPException(status_code=404, detail="Digital Key not found")
    
    # Check if validation failed
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result

@router.delete("/{key_id}", response_model=dict)
def delete_digital_key(key_id: int, db: Session = Depends(get_db)):
    """Delete a digital key and its cloud storage backup."""
    success = digital_key_service.delete_digital_key(db, key_id)
    if not success:
        raise HTTPException(status_code=404, detail="Digital Key not found")
    return {"detail": "Digital Key deleted successfully"}

@router.get("/cloud/uploads/list", response_model=list)
def list_cloud_uploads():
    """List all digital keys uploaded to local cloud storage."""
    uploads = list_all_uploads()
    if not uploads:
        return {"message": "No uploads found"}
    return uploads

@router.get("/cloud/download/{key_id}/{key_name}", response_model=dict)
def download_from_cloud(key_id: int, key_name: str):
    """Download a digital key backup from local cloud storage."""
    data = download_data_from_cloud(key_id, key_name)
    if data is None:
        raise HTTPException(status_code=404, detail="Data not found in cloud storage")
    return data