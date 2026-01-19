import os
import json
import shutil
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
from app.core.config import LOCAL_STORAGE_PATH, STORAGE_BUCKET_NAME, PERMISSIONS_BUCKET_NAME


def initialize_storage() -> None:
    """
    Initialize local cloud storage directories.
    Creates the necessary folder structure for local storage.
    """
    try:
        storage_path = Path(LOCAL_STORAGE_PATH) / STORAGE_BUCKET_NAME
        storage_path.mkdir(parents=True, exist_ok=True)
        metadata_path = storage_path / ".metadata"
        metadata_path.mkdir(exist_ok=True)
        print(f"Local storage initialized at: {storage_path}")
    except Exception as e:
        print(f"Failed to initialize storage: {e}")
        raise


def upload_data_to_cloud(data: Dict[str, Any], key_id: int, key_name: str) -> bool:
    """
    Upload digital key data to local cloud storage as JSON.
    
    Args:
        data (Dict[str, Any]): The data to upload (digital key information).
        key_id (int): The unique identifier for the digital key.
        key_name (str): The name of the digital key.
        
    Returns:
        bool: True if upload is successful, False otherwise.
    """
    try:
        initialize_storage()
        
        storage_path = Path(LOCAL_STORAGE_PATH) / STORAGE_BUCKET_NAME
        
        # Create a unique file path using key_id and key_name
        file_name = f"{key_id}_{key_name.replace(' ', '_')}.json"
        file_path = storage_path / file_name
        
        # Add metadata
        upload_data = {
            "id": key_id,
            "key_name": data.get("key_name"),
            "owner": data.get("owner"),
            "uploaded_at": datetime.utcnow().isoformat(),
            "original_data": data
        }
        
        # Write to local storage
        with open(file_path, 'w') as f:
            json.dump(upload_data, f, indent=2)
        
        print(f"✓ Data uploaded successfully to: {file_path}")
        
        # Update metadata index
        _update_metadata_index(key_id, key_name, str(file_path))
        
        return True
        
    except Exception as e:
        print(f"✗ Upload failed: {e}")
        return False


def download_data_from_cloud(key_id: int, key_name: str) -> Optional[Dict[str, Any]]:
    """
    Download digital key data from local cloud storage.
    
    Args:
        key_id (int): The unique identifier for the digital key.
        key_name (str): The name of the digital key.
        
    Returns:
        Optional[Dict[str, Any]]: The downloaded data or None if not found.
    """
    try:
        storage_path = Path(LOCAL_STORAGE_PATH) / STORAGE_BUCKET_NAME
        file_name = f"{key_id}_{key_name.replace(' ', '_')}.json"
        file_path = storage_path / file_name
        
        if not file_path.exists():
            print(f"✗ File not found: {file_path}")
            return None
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        print(f"✓ Data downloaded successfully from: {file_path}")
        return data
        
    except Exception as e:
        print(f"✗ Download failed: {e}")
        return None


def delete_data_from_cloud(key_id: int, key_name: str) -> bool:
    """
    Delete digital key data from local cloud storage.
    
    Args:
        key_id (int): The unique identifier for the digital key.
        key_name (str): The name of the digital key.
        
    Returns:
        bool: True if deletion is successful, False otherwise.
    """
    try:
        storage_path = Path(LOCAL_STORAGE_PATH) / STORAGE_BUCKET_NAME
        file_name = f"{key_id}_{key_name.replace(' ', '_')}.json"
        file_path = storage_path / file_name
        
        if not file_path.exists():
            print(f"✗ File not found: {file_path}")
            return False
        
        os.remove(file_path)
        _remove_from_metadata_index(key_id, key_name)
        
        print(f"✓ Data deleted successfully: {file_path}")
        return True
        
    except Exception as e:
        print(f"✗ Deletion failed: {e}")
        return False


def list_all_uploads() -> list[Dict[str, Any]]:
    """
    List all uploaded digital key data from local storage.
    
    Returns:
        list[Dict[str, Any]]: List of all uploaded files metadata.
    """
    try:
        storage_path = Path(LOCAL_STORAGE_PATH) / STORAGE_BUCKET_NAME
        
        if not storage_path.exists():
            return []
        
        files = []
        for file_path in storage_path.glob("*.json"):
            with open(file_path, 'r') as f:
                data = json.load(f)
                files.append(data)
        
        print(f"✓ Found {len(files)} uploaded files")
        return files
        
    except Exception as e:
        print(f"✗ Failed to list uploads: {e}")
        return []


def _update_metadata_index(key_id: int, key_name: str, file_path: str) -> None:
    """
    Update metadata index for tracking uploaded files.
    """
    try:
        storage_path = Path(LOCAL_STORAGE_PATH) / STORAGE_BUCKET_NAME / ".metadata"
        index_file = storage_path / "index.json"
        
        # Load existing index
        if index_file.exists():
            with open(index_file, 'r') as f:
                index = json.load(f)
        else:
            index = {"files": []}
        
        # Add entry if not exists
        entry = {"id": key_id, "key_name": key_name, "file_path": file_path, "indexed_at": datetime.utcnow().isoformat()}
        
        # Remove old entry if exists
        index["files"] = [f for f in index["files"] if f["id"] != key_id]
        index["files"].append(entry)
        
        # Write updated index
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)
            
    except Exception as e:
        print(f"Failed to update metadata index: {e}")


def _remove_from_metadata_index(key_id: int, key_name: str) -> None:
    """
    Remove entry from metadata index.
    """
    try:
        storage_path = Path(LOCAL_STORAGE_PATH) / STORAGE_BUCKET_NAME / ".metadata"
        index_file = storage_path / "index.json"
        
        if not index_file.exists():
            return
        
        with open(index_file, 'r') as f:
            index = json.load(f)
        
        # Remove entry
        index["files"] = [f for f in index["files"] if f["id"] != key_id]
        
        # Write updated index
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)
            
    except Exception as e:
        print(f"Failed to remove from metadata index: {e}")


# ============================================================================
# PERMISSION DATA STORAGE FUNCTIONS
# ============================================================================

def upload_permission_to_cloud(permission_data: Dict[str, Any], permission_id: int) -> bool:
    """
    Upload permission data to local cloud storage as JSON.
    
    Args:
        permission_data (Dict[str, Any]): The permission data to upload.
        permission_id (int): The unique identifier for the permission.
        
    Returns:
        bool: True if upload is successful, False otherwise.
    """
    try:
        initialize_storage()
        
        storage_path = Path(LOCAL_STORAGE_PATH) / PERMISSIONS_BUCKET_NAME
        storage_path.mkdir(parents=True, exist_ok=True)
        
        # Create a unique file path using permission_id
        file_name = f"perm_{permission_id}.json"
        file_path = storage_path / file_name
        
        # Add metadata
        upload_data = {
            "id": permission_id,
            "user_id": permission_data.get("user_id"),
            "machine_id": permission_data.get("machine_id"),
            "digital_key_id": permission_data.get("digital_key_id"),
            "permission_level": permission_data.get("permission_level"),
            "is_active": permission_data.get("is_active"),
            "uploaded_at": datetime.utcnow().isoformat(),
            "original_data": permission_data
        }
        
        # Write to local storage
        with open(file_path, 'w') as f:
            json.dump(upload_data, f, indent=2)
        
        print(f"✓ Permission data uploaded successfully to: {file_path}")
        
        # Update metadata index
        _update_permission_metadata_index(permission_id, str(file_path))
        
        return True
        
    except Exception as e:
        print(f"✗ Permission upload failed: {e}")
        return False


def download_permission_from_cloud(permission_id: int) -> Optional[Dict[str, Any]]:
    """
    Download permission data from local cloud storage.
    
    Args:
        permission_id (int): The unique identifier for the permission.
        
    Returns:
        Optional[Dict[str, Any]]: The downloaded data or None if not found.
    """
    try:
        storage_path = Path(LOCAL_STORAGE_PATH) / PERMISSIONS_BUCKET_NAME
        file_name = f"perm_{permission_id}.json"
        file_path = storage_path / file_name
        
        if not file_path.exists():
            print(f"✗ Permission file not found: {file_path}")
            return None
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        print(f"✓ Permission data downloaded successfully from: {file_path}")
        return data
        
    except Exception as e:
        print(f"✗ Permission download failed: {e}")
        return None


def delete_permission_from_cloud(permission_id: int) -> bool:
    """
    Delete permission data from local cloud storage.
    
    Args:
        permission_id (int): The unique identifier for the permission.
        
    Returns:
        bool: True if deletion is successful, False otherwise.
    """
    try:
        storage_path = Path(LOCAL_STORAGE_PATH) / PERMISSIONS_BUCKET_NAME
        file_name = f"perm_{permission_id}.json"
        file_path = storage_path / file_name
        
        if not file_path.exists():
            print(f"✗ Permission file not found: {file_path}")
            return False
        
        os.remove(file_path)
        _remove_permission_from_metadata_index(permission_id)
        
        print(f"✓ Permission data deleted successfully: {file_path}")
        return True
        
    except Exception as e:
        print(f"✗ Permission deletion failed: {e}")
        return False


def list_all_permissions() -> list[Dict[str, Any]]:
    """
    List all permission data from local storage.
    
    Returns:
        list[Dict[str, Any]]: List of all permission files metadata.
    """
    try:
        storage_path = Path(LOCAL_STORAGE_PATH) / PERMISSIONS_BUCKET_NAME
        
        if not storage_path.exists():
            return []
        
        files = []
        for file_path in storage_path.glob("*.json"):
            with open(file_path, 'r') as f:
                data = json.load(f)
                files.append(data)
        
        print(f"✓ Found {len(files)} permission files")
        return files
        
    except Exception as e:
        print(f"✗ Failed to list permissions: {e}")
        return []


def update_permission_in_cloud(permission_data: Dict[str, Any], permission_id: int) -> bool:
    """
    Update existing permission data in local cloud storage.
    
    Args:
        permission_data (Dict[str, Any]): The updated permission data.
        permission_id (int): The unique identifier for the permission.
        
    Returns:
        bool: True if update is successful, False otherwise.
    """
    try:
        storage_path = Path(LOCAL_STORAGE_PATH) / PERMISSIONS_BUCKET_NAME
        file_name = f"perm_{permission_id}.json"
        file_path = storage_path / file_name
        
        if not file_path.exists():
            print(f"✗ Permission file not found: {file_path}")
            return False
        
        # Add metadata
        upload_data = {
            "id": permission_id,
            "user_id": permission_data.get("user_id"),
            "machine_id": permission_data.get("machine_id"),
            "digital_key_id": permission_data.get("digital_key_id"),
            "permission_level": permission_data.get("permission_level"),
            "is_active": permission_data.get("is_active"),
            "updated_at": datetime.utcnow().isoformat(),
            "original_data": permission_data
        }
        
        # Write to local storage
        with open(file_path, 'w') as f:
            json.dump(upload_data, f, indent=2)
        
        print(f"✓ Permission data updated successfully in: {file_path}")
        return True
        
    except Exception as e:
        print(f"✗ Permission update failed: {e}")
        return False


def _update_permission_metadata_index(permission_id: int, file_path: str) -> None:
    """
    Update metadata index for tracking uploaded permission files.
    """
    try:
        storage_path = Path(LOCAL_STORAGE_PATH) / PERMISSIONS_BUCKET_NAME / ".metadata"
        storage_path.mkdir(parents=True, exist_ok=True)
        index_file = storage_path / "permissions_index.json"
        
        # Load existing index
        if index_file.exists():
            with open(index_file, 'r') as f:
                index = json.load(f)
        else:
            index = {"permissions": []}
        
        # Add entry if not exists
        entry = {"id": permission_id, "file_path": file_path, "indexed_at": datetime.utcnow().isoformat()}
        
        # Remove old entry if exists
        index["permissions"] = [p for p in index["permissions"] if p["id"] != permission_id]
        index["permissions"].append(entry)
        
        # Write updated index
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)
            
    except Exception as e:
        print(f"Failed to update permission metadata index: {e}")


def _remove_permission_from_metadata_index(permission_id: int) -> None:
    """
    Remove permission entry from metadata index.
    """
    try:
        storage_path = Path(LOCAL_STORAGE_PATH) / PERMISSIONS_BUCKET_NAME / ".metadata"
        index_file = storage_path / "permissions_index.json"
        
        if not index_file.exists():
            return
        
        with open(index_file, 'r') as f:
            index = json.load(f)
        
        # Remove entry
        index["permissions"] = [p for p in index["permissions"] if p["id"] != permission_id]
        
        # Write updated index
        with open(index_file, 'w') as f:
            json.dump(index, f, indent=2)
            
    except Exception as e:
        print(f"Failed to remove permission from metadata index: {e}")