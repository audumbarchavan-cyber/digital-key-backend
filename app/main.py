from fastapi import FastAPI
from app.api.v1.digital_key import router as digital_key_router

app = FastAPI(title="Digital Key Backend API")

app.include_router(digital_key_router, prefix="/api/v1")

@app.get("/")
def health_check():
    return {"status": "Digital Key Backend is running"}