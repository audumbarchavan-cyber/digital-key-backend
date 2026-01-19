from sqlalchemy.orm import Session
from datetime import datetime
from app.models.permission import UserMachinePermission, PermissionLevel
from app.models.digital_key import DigitalKey
from app.schemas.access import UserMachinePermissionCreate, UserMachinePermissionUpdate
from app.utils.cloud import (
    upload_permission_to_cloud,
    delete_permission_from_cloud,
    update_permission_in_cloud
)


def grant_user_machine_access(db: Session, permission: UserMachinePermissionCreate) -> UserMachinePermission | dict:
    """Grant a user access to a machine with a specific digital key.
    
    Validates that the digital key belongs to the machine being granted access to.
    Uploads permission data to cloud storage.
    """
    # Validate that the digital key exists and belongs to the machine
    digital_key = db.query(DigitalKey).filter(DigitalKey.id == permission.digital_key_id).first()
    if not digital_key:
        return {"error": f"Digital key with ID {permission.digital_key_id} does not exist"}
    
    if digital_key.machine_id != permission.machine_id:
        return {"error": f"Digital key {permission.digital_key_id} does not belong to machine {permission.machine_id}."}
    
    db_permission = UserMachinePermission(
        user_id=permission.user_id,
        machine_id=permission.machine_id,
        digital_key_id=permission.digital_key_id,
        permission_level=permission.permission_level,
        is_active=True
    )
    db.add(db_permission)
    db.commit()
    db.refresh(db_permission)
    
    # Upload permission data to cloud storage
    permission_data = {
        "user_id": db_permission.user_id,
        "machine_id": db_permission.machine_id,
        "digital_key_id": db_permission.digital_key_id,
        "permission_level": db_permission.permission_level.value,
        "is_active": db_permission.is_active,
        "created_at": db_permission.created_at.isoformat() if db_permission.created_at else None
    }
    upload_permission_to_cloud(permission_data, db_permission.id)
    
    return db_permission


def get_permission_by_id(db: Session, permission_id: int) -> UserMachinePermission | None:
    """Get a permission by ID."""
    return db.query(UserMachinePermission).filter(UserMachinePermission.id == permission_id).first()


def get_user_permissions(db: Session, user_id: int) -> list[UserMachinePermission]:
    """Get all permissions for a specific user."""
    return db.query(UserMachinePermission).filter(
        UserMachinePermission.user_id == user_id,
        UserMachinePermission.is_active == True
    ).all()


def get_machine_permissions(db: Session, machine_id: int) -> list[UserMachinePermission]:
    """Get all permissions for a specific machine."""
    return db.query(UserMachinePermission).filter(
        UserMachinePermission.machine_id == machine_id,
        UserMachinePermission.is_active == True
    ).all()


def get_user_machine_permission(db: Session, user_id: int, machine_id: int) -> UserMachinePermission | None:
    """Get permission for a user accessing a specific machine."""
    return db.query(UserMachinePermission).filter(
        UserMachinePermission.user_id == user_id,
        UserMachinePermission.machine_id == machine_id,
        UserMachinePermission.is_active == True
    ).first()


def get_all_permissions(db: Session, skip: int = 0, limit: int = 100) -> list[UserMachinePermission]:
    """Get all permissions with pagination."""
    return db.query(UserMachinePermission).offset(skip).limit(limit).all()


def update_permission(db: Session, permission_id: int, permission_update: UserMachinePermissionUpdate) -> UserMachinePermission | None:
    """Update a permission and upload to cloud storage."""
    db_permission = db.query(UserMachinePermission).filter(UserMachinePermission.id == permission_id).first()
    if db_permission:
        if permission_update.permission_level is not None:
            db_permission.permission_level = permission_update.permission_level
        if permission_update.is_active is not None:
            db_permission.is_active = permission_update.is_active
        db.commit()
        db.refresh(db_permission)
        
        # Upload updated permission data to cloud storage
        permission_data = {
            "user_id": db_permission.user_id,
            "machine_id": db_permission.machine_id,
            "digital_key_id": db_permission.digital_key_id,
            "permission_level": db_permission.permission_level.value,
            "is_active": db_permission.is_active,
            "updated_at": datetime.utcnow().isoformat()
        }
        update_permission_in_cloud(permission_data, db_permission.id)
    
    return db_permission


def revoke_permission(db: Session, permission_id: int) -> bool:
    """Revoke a user's access to a machine and delete from cloud storage."""
    db_permission = db.query(UserMachinePermission).filter(UserMachinePermission.id == permission_id).first()
    if db_permission:
        db_permission.is_active = False
        db_permission.revoked_at = datetime.utcnow()
        db.commit()
        
        # Update in cloud storage
        permission_data = {
            "user_id": db_permission.user_id,
            "machine_id": db_permission.machine_id,
            "digital_key_id": db_permission.digital_key_id,
            "permission_level": db_permission.permission_level.value,
            "is_active": db_permission.is_active,
            "revoked_at": db_permission.revoked_at.isoformat() if db_permission.revoked_at else None
        }
        update_permission_in_cloud(permission_data, db_permission.id)
        
        return True
    return False


def revoke_user_machine_access(db: Session, user_id: int, machine_id: int) -> bool:
    """Revoke a user's access to a specific machine."""
    db_permission = db.query(UserMachinePermission).filter(
        UserMachinePermission.user_id == user_id,
        UserMachinePermission.machine_id == machine_id
    ).first()
    if db_permission:
        db_permission.is_active = False
        db_permission.revoked_at = datetime.utcnow()
        db.commit()
        return True
    return False


def delete_permission(db: Session, permission_id: int) -> bool:
    """Delete a permission record and from cloud storage."""
    db_permission = db.query(UserMachinePermission).filter(UserMachinePermission.id == permission_id).first()
    if db_permission:
        db.delete(db_permission)
        db.commit()
        
        # Delete from cloud storage
        delete_permission_from_cloud(permission_id)
        
        return True
    return False
