"""
Database Utility Script: Clear or Reset Database
Provides easy-to-use functions for managing database records
"""

import os
import sys
from sqlalchemy.orm import Session
from app.db.database import SessionLocal, engine
from app.models.digital_key import DigitalKey, Base
from app.models.user import User
from app.models.machine import Machine
from app.models.permission import UserMachinePermission

def clear_all_data():
    """Delete all records from all tables while preserving table structure"""
    db = SessionLocal()
    try:
        # Delete in order to respect foreign key constraints
        deleted_permissions = db.query(UserMachinePermission).delete()
        deleted_keys = db.query(DigitalKey).delete()
        deleted_users = db.query(User).delete()
        deleted_machines = db.query(Machine).delete()
        
        db.commit()
        
        print("✓ Database cleared successfully!")
        print(f"  - Permissions deleted: {deleted_permissions}")
        print(f"  - Digital keys deleted: {deleted_keys}")
        print(f"  - Users deleted: {deleted_users}")
        print(f"  - Machines deleted: {deleted_machines}")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error clearing database: {e}")
    finally:
        db.close()

def reset_database():
    """Drop all tables and recreate them (hard reset)"""
    try:
        print("Resetting database...")
        
        # Drop all tables
        Base.metadata.drop_all(bind=engine)
        print("✓ All tables dropped")
        
        # Recreate all tables
        Base.metadata.create_all(bind=engine)
        print("✓ All tables recreated (empty)")
        
        print("\n✓ Database reset successfully!")
        
    except Exception as e:
        print(f"✗ Error resetting database: {e}")

def delete_by_id(entity_type: str, entity_id: int):
    """Delete a specific record by ID"""
    db = SessionLocal()
    try:
        entity_map = {
            'digital_key': DigitalKey,
            'user': User,
            'machine': Machine,
            'permission': UserMachinePermission,
        }
        
        if entity_type not in entity_map:
            print(f"✗ Unknown entity type: {entity_type}")
            print(f"  Available types: {', '.join(entity_map.keys())}")
            return
        
        EntityClass = entity_map[entity_type]
        entity = db.query(EntityClass).filter(EntityClass.id == entity_id).first()
        
        if entity:
            db.delete(entity)
            db.commit()
            print(f"✓ {entity_type} {entity_id} deleted successfully")
        else:
            print(f"✗ {entity_type} {entity_id} not found")
            
    except Exception as e:
        db.rollback()
        print(f"✗ Error deleting {entity_type}: {e}")
    finally:
        db.close()

def delete_table(table_name: str):
    """Delete all records from a specific table"""
    db = SessionLocal()
    try:
        table_map = {
            'digital_keys': DigitalKey,
            'users': User,
            'machines': Machine,
            'permissions': UserMachinePermission,
        }
        
        if table_name not in table_map:
            print(f"✗ Unknown table: {table_name}")
            print(f"  Available tables: {', '.join(table_map.keys())}")
            return
        
        TableClass = table_map[table_name]
        count = db.query(TableClass).delete()
        db.commit()
        
        print(f"✓ {count} records deleted from {table_name}")
        
    except Exception as e:
        db.rollback()
        print(f"✗ Error clearing table: {e}")
    finally:
        db.close()

def delete_database_file():
    """Delete the SQLite database file"""
    try:
        if os.path.exists("digital_key.db"):
            os.remove("digital_key.db")
            print("✓ Database file deleted")
            print("  Note: Restart the server to recreate the database")
        else:
            print("✗ Database file not found")
    except Exception as e:
        print(f"✗ Error deleting database file: {e}")

def display_menu():
    """Display interactive menu"""
    while True:
        print("\n" + "="*50)
        print("DATABASE MANAGEMENT MENU")
        print("="*50)
        print("1. Clear all data (keep tables)")
        print("2. Reset database (drop & recreate tables)")
        print("3. Delete specific record")
        print("4. Clear specific table")
        print("5. Delete database file")
        print("6. Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-6): ").strip()
        
        if choice == '1':
            confirm = input("Are you sure? This will delete all data (y/n): ").lower()
            if confirm == 'y':
                clear_all_data()
                
        elif choice == '2':
            confirm = input("Are you sure? This will reset the entire database (y/n): ").lower()
            if confirm == 'y':
                reset_database()
                
        elif choice == '3':
            entity_type = input("Entity type (digital_key/user/machine/permission): ").strip().lower()
            try:
                entity_id = int(input("Entity ID: "))
                delete_by_id(entity_type, entity_id)
            except ValueError:
                print("✗ Invalid ID")
                
        elif choice == '4':
            table_name = input("Table name (digital_keys/users/machines/permissions): ").strip().lower()
            confirm = input(f"Delete all records from {table_name}? (y/n): ").lower()
            if confirm == 'y':
                delete_table(table_name)
                
        elif choice == '5':
            confirm = input("Delete database file? (y/n): ").lower()
            if confirm == 'y':
                delete_database_file()
                
        elif choice == '6':
            print("Exiting...")
            break
            
        else:
            print("✗ Invalid choice")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == "clear":
            clear_all_data()
            
        elif command == "reset":
            confirm = input("Are you sure? This will reset the entire database (y/n): ").lower()
            if confirm == 'y':
                reset_database()
                
        elif command == "delete-file":
            confirm = input("Delete database file? (y/n): ").lower()
            if confirm == 'y':
                delete_database_file()
                
        elif command == "delete":
            if len(sys.argv) > 3:
                entity_type = sys.argv[2]
                entity_id = int(sys.argv[3])
                delete_by_id(entity_type, entity_id)
            else:
                print("Usage: python clear_database.py delete <entity_type> <id>")
                
        elif command == "clear-table":
            if len(sys.argv) > 2:
                table_name = sys.argv[2]
                delete_table(table_name)
            else:
                print("Usage: python clear_database.py clear-table <table_name>")
                
        elif command == "menu":
            display_menu()
            
        else:
            print("Usage: python clear_database.py [clear|reset|delete-file|delete|clear-table|menu]")
            print("\nExamples:")
            print("  python clear_database.py clear              - Clear all data")
            print("  python clear_database.py reset             - Reset database")
            print("  python clear_database.py delete user 5     - Delete user with ID 5")
            print("  python clear_database.py clear-table users - Delete all users")
            print("  python clear_database.py delete-file       - Delete database file")
            print("  python clear_database.py menu              - Interactive menu")
    else:
        display_menu()
