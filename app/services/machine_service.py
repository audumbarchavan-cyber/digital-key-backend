from sqlalchemy.orm import Session
from app.models.machine import Machine, MachineType
from app.schemas.permission import MachineCreate, MachineUpdate


def create_machine(db: Session, machine: MachineCreate) -> Machine:
    """Create a new machine."""
    db_machine = Machine(
        machine_name=machine.machine_name,
        machine_type=machine.machine_type,
        ip_address=machine.ip_address,
        description=machine.description
    )
    db.add(db_machine)
    db.commit()
    db.refresh(db_machine)
    return db_machine


def get_machine_by_id(db: Session, machine_id: int) -> Machine | None:
    """Get machine by ID."""
    return db.query(Machine).filter(Machine.id == machine_id).first()


def get_machine_by_name(db: Session, machine_name: str) -> Machine | None:
    """Get machine by name."""
    return db.query(Machine).filter(Machine.machine_name == machine_name).first()


def get_all_machines(db: Session, skip: int = 0, limit: int = 100) -> list[Machine]:
    """Get all machines with pagination."""
    return db.query(Machine).offset(skip).limit(limit).all()


def get_machines_by_type(db: Session, machine_type: MachineType) -> list[Machine]:
    """Get all machines of a specific type."""
    return db.query(Machine).filter(Machine.machine_type == machine_type).all()


def get_active_machines(db: Session) -> list[Machine]:
    """Get all active machines."""
    return db.query(Machine).filter(Machine.is_active == 1).all()


def update_machine(db: Session, machine_id: int, machine_update: MachineUpdate) -> Machine | None:
    """Update a machine."""
    db_machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if db_machine:
        if machine_update.machine_name is not None:
            db_machine.machine_name = machine_update.machine_name
        if machine_update.machine_type is not None:
            db_machine.machine_type = machine_update.machine_type
        if machine_update.ip_address is not None:
            db_machine.ip_address = machine_update.ip_address
        if machine_update.description is not None:
            db_machine.description = machine_update.description
        if machine_update.is_active is not None:
            db_machine.is_active = machine_update.is_active
        db.commit()
        db.refresh(db_machine)
    return db_machine


def delete_machine(db: Session, machine_id: int) -> bool:
    """Delete a machine."""
    db_machine = db.query(Machine).filter(Machine.id == machine_id).first()
    if db_machine:
        db.delete(db_machine)
        db.commit()
        return True
    return False
