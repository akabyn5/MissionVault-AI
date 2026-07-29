from fastapi import APIRouter, Query

from app.schemas.telemetry import Telemetry

from app.services.telemetry_service import (
    save_telemetry,
    get_all_telemetry,
    get_latest_telemetry,
    get_telemetry_stats,
    get_health_metrics,
    get_time_statistics,
    get_mission_summary,
    get_trend_analysis,
    get_dashboard_data,
    get_anomalies,
    get_recent_anomalies,
    get_telemetry_by_severity,
    get_telemetry_by_satellite,
    search_telemetry
)

from app.services.analysis_service import analyze_telemetry

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

    # Analyze telemetry
    analysis = analyze_telemetry(data)

    # Store telemetry
    save_telemetry(data, analysis)

    return {
        "message": "Telemetry received successfully",
        "satellite": data.satellite_id,
        "analysis": analysis
    }


@router.get("/telemetry")
def list_telemetry():
    return get_all_telemetry()


@router.get("/telemetry/latest")
def latest_telemetry():
    return get_latest_telemetry()


@router.get("/telemetry/stats")
def telemetry_stats():
    return get_telemetry_stats()

@router.get("/telemetry/metrics")
def telemetry_metrics():
    return get_health_metrics()

@router.get("/telemetry/time")
def telemetry_time():
    return get_time_statistics()

@router.get("/telemetry/summary")
def telemetry_summary():
    return get_mission_summary()

@router.get("/telemetry/trends")
def telemetry_trends():
    return get_trend_analysis()

@router.get("/telemetry/anomalies")
def telemetry_anomalies():
    return get_anomalies()

@router.get("/telemetry/severity/{level}")
def telemetry_by_severity(level: str):
    return get_telemetry_by_severity(level)

@router.get("/telemetry/satellite/{satellite_id}")
def telemetry_by_satellite(satellite_id: str):
    return get_telemetry_by_satellite(satellite_id)

@router.get("/telemetry/search")
def telemetry_search(
    satellite_id: str | None = Query(default=None),
    severity: str | None = Query(default=None)
):
    return search_telemetry(
        satellite_id=satellite_id,
        severity=severity
    )

@router.get("/telemetry/dashboard")
def telemetry_dashboard():
    return get_dashboard_data()

