from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.models.machine import Base, Machine
from app.schemas.permission import MachineCreate, MachineUpdate, MachineResponse
from app.services import machine_service

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/machines", tags=["Machines"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=MachineResponse)
def create_machine(machine: MachineCreate, db: Session = Depends(get_db)):
    """Create a new machine."""
    # Check if machine name already exists
    existing_machine = machine_service.get_machine_by_name(db, machine.machine_name)
    if existing_machine:
        raise HTTPException(status_code=400, detail="Machine name already exists")
    
    return machine_service.create_machine(db, machine)


@router.get("/{machine_id}", response_model=MachineResponse)
def read_machine(machine_id: int, db: Session = Depends(get_db)):
    """Get a machine by ID."""
    db_machine = machine_service.get_machine_by_id(db, machine_id)
    if db_machine is None:
        raise HTTPException(status_code=404, detail="Machine not found")
    return db_machine


@router.get("/name/{machine_name}", response_model=MachineResponse)
def read_machine_by_name(machine_name: str, db: Session = Depends(get_db)):
    """Get a machine by name."""
    db_machine = machine_service.get_machine_by_name(db, machine_name)
    if db_machine is None:
        raise HTTPException(status_code=404, detail="Machine not found")
    return db_machine


@router.get("/", response_model=list[MachineResponse])
def read_all_machines(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
    """Get all machines with pagination."""
    return machine_service.get_all_machines(db, skip=skip, limit=limit)


@router.get("/type/{machine_type}", response_model=list[MachineResponse])
def read_machines_by_type(machine_type: str, db: Session = Depends(get_db)):
    """Get all machines of a specific type."""
    try:
        from app.models.machine import MachineType
        machine_type_enum = MachineType[machine_type.upper()]
        return machine_service.get_machines_by_type(db, machine_type_enum)
    except KeyError:
        raise HTTPException(status_code=400, detail="Invalid machine type")


@router.get("/active/", response_model=list[MachineResponse])
def read_active_machines(db: Session = Depends(get_db)):
    """Get all active machines."""
    return machine_service.get_active_machines(db)


@router.put("/{machine_id}", response_model=MachineResponse)
def update_machine(machine_id: int, machine_update: MachineUpdate, db: Session = Depends(get_db)):
    """Update a machine."""
    db_machine = machine_service.update_machine(db, machine_id, machine_update)
    if db_machine is None:
        raise HTTPException(status_code=404, detail="Machine not found")
    return db_machine


@router.delete("/{machine_id}", response_model=dict)
def delete_machine(machine_id: int, db: Session = Depends(get_db)):
    """Delete a machine."""
    success = machine_service.delete_machine(db, machine_id)
    if not success:
        raise HTTPException(status_code=404, detail="Machine not found")
    return {"detail": "Machine deleted successfully"}
