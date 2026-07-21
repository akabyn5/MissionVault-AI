from fastapi import APIRouter
from app.schemas.telemetry import Telemetry
from app.services.telemetry_service import save_telemetry

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "ok",
        "service": "MissionVault AI"
    }


@router.post("/telemetry")
def receive_telemetry(data: Telemetry):
    save_telemetry(data)

    return {
        "message": "Telemetry received successfully",
        "satellite": data.satellite_id
    }