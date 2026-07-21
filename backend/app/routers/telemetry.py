from fastapi import APIRouter
from app.schemas.telemetry import Telemetry
from app.services.telemetry_service import (
    save_telemetry,
    get_all_telemetry
)

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "MissionVault AI"
    }


@router.post("/telemetry")
def receive_telemetry(data: Telemetry):
    print("\nTelemetry received:")
    print(data)
    save_telemetry(data)

    return {
        "message": "Telemetry received successfully",
        "satellite": data.satellite_id
    }

@router.get("/telemetry")
def list_telemetry():
    return get_all_telemetry()