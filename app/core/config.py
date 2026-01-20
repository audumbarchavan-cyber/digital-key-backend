import os

DATABASE_URL = "sqlite:///./digital_key.db"

# Local Cloud Storage Configuration
LOCAL_STORAGE_PATH = os.getenv("LOCAL_STORAGE_PATH", "./local_storage")
STORAGE_BUCKET_NAME = "digital-keys"
PERMISSIONS_BUCKET_NAME = "permissions"