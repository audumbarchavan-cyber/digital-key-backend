from fastapi import FastAPI
from app.api.v1.digital_key import router as digital_key_router
from app.api.v1.users import router as users_router
from app.api.v1.machines import router as machines_router
from app.api.v1.permissions import router as permissions_router

app = FastAPI(title="Digital Key Backend API")

app.include_router(digital_key_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(machines_router, prefix="/api/v1")
app.include_router(permissions_router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "Digital Key Backend is running"}