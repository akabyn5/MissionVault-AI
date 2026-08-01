from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.telemetry import router as telemetry_router

app = FastAPI(
    title="MissionVault AI API",
    description="Backend API for secure satellite telemetry and anomaly detection",
    version="0.1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(telemetry_router)

@app.get("/")
def root():
    return {
        "message": "MissionVault AI Backend Running",
        "version": "0.1.0"
    }