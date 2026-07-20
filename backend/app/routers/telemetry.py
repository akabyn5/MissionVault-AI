from fastapi import APIRouter
from app.schemas.telemetry import Telemetry

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

    return {
        "message": "Telemetry received successfully",
        "satellite": data.satellite_id
    }