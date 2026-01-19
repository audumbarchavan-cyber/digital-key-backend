from sqlalchemy.orm import Session
from app.models.user import User, UserType
from app.schemas.user import UserCreate, UserUpdate


def create_user(db: Session, user: UserCreate) -> User:
    """Create a new user."""
    db_user = User(
        username=user.username,
        user_type=user.user_type,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> User | None:
    """Get user by username."""
    return db.query(User).filter(User.username == username).first()


def get_all_users(db: Session, skip: int = 0, limit: int = 100) -> list[User]:
    """Get all users with pagination."""
    return db.query(User).offset(skip).limit(limit).all()


def get_users_by_type(db: Session, user_type: UserType) -> list[User]:
    """Get all users of a specific type."""
    return db.query(User).filter(User.user_type == user_type).all()


def update_user(db: Session, user_id: int, user_update: UserUpdate) -> User | None:
    """Update a user."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        if user_update.username is not None:
            db_user.username = user_update.username
        if user_update.user_type is not None:
            db_user.user_type = user_update.user_type
        if user_update.email is not None:
            db_user.email = user_update.email
        db.commit()
        db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """Delete a user."""
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
        return True
    return False
