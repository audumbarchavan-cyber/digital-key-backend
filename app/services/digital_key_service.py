from sqlalchemy.orm import Session
from app.models.digital_key import DigitalKey
from app.models.machine import Machine
from app.schemas.digital_key import DigitalKeyCreate
from app.utils.cloud import upload_data_to_cloud, delete_data_from_cloud

def create_digital_key(db: Session, digital_key: DigitalKeyCreate) -> DigitalKey | dict:
    # Validate that the machine exists
    machine = db.query(Machine).filter(Machine.id == digital_key.machine_id).first()
    if not machine:
        return {"error": f"Machine with ID {digital_key.machine_id} does not exist"}
    
    db_digital_key = DigitalKey(
        key_name=digital_key.key_name,
        key_value=digital_key.key_value,
        owner=digital_key.owner,
        machine_id=digital_key.machine_id
    )
    db.add(db_digital_key)
    db.commit()
    db.refresh(db_digital_key)
    
    # Upload to local cloud storage
    upload_data_to_cloud(
        data={
            "key_name": db_digital_key.key_name,
            "key_value": db_digital_key.key_value,
            "owner": db_digital_key.owner,
            "machine_id": db_digital_key.machine_id
        },
        key_id=db_digital_key.id,
        key_name=db_digital_key.key_name
    )
    
    return db_digital_key

def get_digital_key_by_id(db: Session, key_id: int) -> DigitalKey | None:
    return db.query(DigitalKey).filter(DigitalKey.id == key_id).first()

def get_all_digital_keys(db: Session) -> list[DigitalKey]:
    return db.query(DigitalKey).all()

def update_digital_key(db: Session, key_id: int, digital_key: DigitalKeyCreate) -> DigitalKey | dict | None:
    db_digital_key = db.query(DigitalKey).filter(DigitalKey.id == key_id).first()
    if not db_digital_key:
        return None
    
    # Validate that the machine exists
    machine = db.query(Machine).filter(Machine.id == digital_key.machine_id).first()
    if not machine:
        return {"error": f"Machine with ID {digital_key.machine_id} does not exist"}
    
    # Delete old cloud storage file
    delete_data_from_cloud(db_digital_key.id, db_digital_key.key_name)
    
    # Update database
    db_digital_key.key_name = digital_key.key_name
    db_digital_key.key_value = digital_key.key_value
    db_digital_key.owner = digital_key.owner
    db_digital_key.machine_id = digital_key.machine_id
    db.commit()
    db.refresh(db_digital_key)
    
    # Upload updated data to cloud storage
    upload_data_to_cloud(
        data={
            "key_name": db_digital_key.key_name,
            "key_value": db_digital_key.key_value,
            "owner": db_digital_key.owner,
            "machine_id": db_digital_key.machine_id
        },
        key_id=db_digital_key.id,
        key_name=db_digital_key.key_name
    )
    
    return db_digital_key

def delete_digital_key(db: Session, key_id: int) -> bool:
    digital_key = db.query(DigitalKey).filter(DigitalKey.id == key_id).first()
    if digital_key:
        # Delete from cloud storage
        delete_data_from_cloud(digital_key.id, digital_key.key_name)
        
        # Delete from database
        db.delete(digital_key)
        db.commit()
        return True
    return False

def get_digital_keys_by_machine(db: Session, machine_id: int) -> list[DigitalKey]:
    """Get all digital keys associated with a specific machine"""
    return db.query(DigitalKey).filter(DigitalKey.machine_id == machine_id).all()

def get_digital_key_by_name(db: Session, key_name: str) -> DigitalKey | None:
    """Get a digital key by its name"""
    return db.query(DigitalKey).filter(DigitalKey.key_name == key_name).first()

def get_digital_keys_by_owner(db: Session, owner: str) -> list[DigitalKey]:
    """Get all digital keys owned by a specific user"""
    return db.query(DigitalKey).filter(DigitalKey.owner == owner).all()