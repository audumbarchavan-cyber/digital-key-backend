from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from app.db.database import SessionLocal, engine
from app.models.permission import Base, UserMachinePermission
from app.models.user import User
from app.models.machine import Machine
from app.schemas.access import (
    UserMachinePermissionCreate,
    UserMachinePermissionUpdate,
    UserMachinePermissionResponse,
    UserAccessResponse
)
from app.services import permission_service
from app.utils.cloud import list_all_permissions, download_permission_from_cloud

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/permissions", tags=["Permissions"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/grant", response_model=UserMachinePermissionResponse)
def grant_access(permission: UserMachinePermissionCreate, db: Session = Depends(get_db)):
    """Grant a user access to a machine with a digital key.
    
    Validates that:
    1. User exists
    2. Machine exists
    3. Digital key exists and belongs to the machine
    4. Permission doesn't already exist
    """
    # Validate user exists
    user = db.query(User).filter(User.id == permission.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Validate machine exists
    machine = db.query(Machine).filter(Machine.id == permission.machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    # Check if permission already exists
    existing_permission = db.query(UserMachinePermission).filter(
        UserMachinePermission.user_id == permission.user_id,
        UserMachinePermission.machine_id == permission.machine_id
    ).first()
    if existing_permission:
        raise HTTPException(status_code=400, detail="Permission already exists for this user-machine pair")
    
    # Grant access (this will validate digital key belongs to machine)
    result = permission_service.grant_user_machine_access(db, permission)
    
    # Check if validation failed
    if isinstance(result, dict) and "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@router.get("/{permission_id}", response_model=UserMachinePermissionResponse)
def read_permission(permission_id: int, db: Session = Depends(get_db)):
    """Get a permission by ID."""
    db_permission = permission_service.get_permission_by_id(db, permission_id)
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission


@router.get("/user/{user_id}", response_model=list[UserMachinePermissionResponse])
def get_user_permissions(user_id: int, db: Session = Depends(get_db)):
    """Get all permissions for a user."""
    # Validate user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return permission_service.get_user_permissions(db, user_id)


@router.get("/machine/{machine_id}", response_model=list[UserMachinePermissionResponse])
def get_machine_permissions(machine_id: int, db: Session = Depends(get_db)):
    """Get all permissions for a machine."""
    # Validate machine exists
    machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    return permission_service.get_machine_permissions(db, machine_id)


@router.get("/user/{user_id}/machine/{machine_id}", response_model=UserMachinePermissionResponse)
def get_user_machine_permission(user_id: int, machine_id: int, db: Session = Depends(get_db)):
    """Get permission for a user accessing a specific machine."""
    db_permission = permission_service.get_user_machine_permission(db, user_id, machine_id)
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission


@router.get("/", response_model=list[UserMachinePermissionResponse])
def read_all_permissions(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    """Get all permissions with pagination."""
    return permission_service.get_all_permissions(db, skip=skip, limit=limit)


@router.put("/{permission_id}", response_model=UserMachinePermissionResponse)
def update_permission(permission_id: int, permission_update: UserMachinePermissionUpdate, db: Session = Depends(get_db)):
    """Update a permission."""
    db_permission = permission_service.update_permission(db, permission_id, permission_update)
    if db_permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")
    return db_permission


@router.post("/{permission_id}/revoke", response_model=dict)
def revoke_permission(permission_id: int, db: Session = Depends(get_db)):
    """Revoke a permission."""
    success = permission_service.revoke_permission(db, permission_id)
    if not success:
        raise HTTPException(status_code=404, detail="Permission not found")
    return {"detail": "Permission revoked successfully"}


@router.post("/user/{user_id}/machine/{machine_id}/revoke", response_model=dict)
def revoke_user_machine_access(user_id: int, machine_id: int, db: Session = Depends(get_db)):
    """Revoke a user's access to a machine."""
    success = permission_service.revoke_user_machine_access(db, user_id, machine_id)
    if not success:
        raise HTTPException(status_code=404, detail="Permission not found")
    return {"detail": "User access revoked successfully"}


@router.delete("/{permission_id}", response_model=dict)
def delete_permission(permission_id: int, db: Session = Depends(get_db)):
    """Delete a permission record."""
    success = permission_service.delete_permission(db, permission_id)
    if not success:
        raise HTTPException(status_code=404, detail="Permission not found")
    return {"detail": "Permission deleted successfully"}


@router.get("/access/user/{user_id}", response_model=list[UserAccessResponse])
def get_user_access_summary(user_id: int, db: Session = Depends(get_db)):
    """Get a summary of a user's access to all machines."""
    # Validate user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    permissions = db.query(UserMachinePermission).filter(
        UserMachinePermission.user_id == user_id,
        UserMachinePermission.is_active == True
    ).all()
    
    access_list = []
    for permission in permissions:
        machine = db.query(Machine).filter(Machine.id == permission.machine_id).first()
        if machine:
            access_list.append(UserAccessResponse(
                user_id=user.id,
                username=user.username,
                machine_id=machine.id,
                machine_name=machine.machine_name,
                permission_level=permission.permission_level,
                is_active=permission.is_active,
                created_at=permission.created_at
            ))
    
    return access_list


@router.get("/access/machine/{machine_id}", response_model=list[dict])
def get_machine_access_summary(machine_id: int, db: Session = Depends(get_db)):
    """Get a summary of all users' access to a machine."""
    # Validate machine exists
    machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if not machine:
        raise HTTPException(status_code=404, detail="Machine not found")
    
    permissions = db.query(UserMachinePermission).filter(
        UserMachinePermission.machine_id == machine_id,
        UserMachinePermission.is_active == True
    ).all()
    
    access_list = []
    for permission in permissions:
        user = db.query(User).filter(User.id == permission.user_id).first()
        if user:
            access_list.append({
                "user_id": user.id,
                "username": user.username,
                "user_type": user.user_type,
                "permission_level": permission.permission_level,
                "is_active": permission.is_active,
                "created_at": permission.created_at
            })
    
    return access_list


# ============================================================================
# CLOUD STORAGE ENDPOINTS FOR PERMISSIONS
# ============================================================================

@router.get("/cloud/uploads/list", response_model=list)
def list_permission_cloud_uploads():
    """List all permission data uploaded to local cloud storage."""
    uploads = list_all_permissions()
    if not uploads:
        return {"message": "No permission uploads found"}
    return uploads


@router.get("/cloud/download/{permission_id}", response_model=dict)
def download_permission_from_cloud_endpoint(permission_id: int):
    """Download a permission backup from local cloud storage."""
    data = download_permission_from_cloud(permission_id)
    if data is None:
        raise HTTPException(status_code=404, detail="Permission data not found in cloud storage")
    return data
