import logging

from datetime import timedelta

from app.schemas.telemetry import Telemetry

# Configure the logger for this module
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# Temporary in-memory storage
telemetry_storage: list[dict] = []


def save_telemetry(data: Telemetry, analysis: dict):
    """
    Store a telemetry packet together with its analysis.
    """

    record = {
        "telemetry": data,
        "analysis": analysis
    }

    telemetry_storage.append(record)

    logger.info("Stored packets: %d", len(telemetry_storage))
    logger.info("Latest record: %s", record)

    return record


def get_all_telemetry() -> list[dict]:
    """
    Return a copy of all stored telemetry records.
    """

    return telemetry_storage.copy()

def get_latest_telemetry() -> dict | None:
    """
    Return the most recent telemetry record, or None if storage is empty.
    """
    if not telemetry_storage:
        logger.warning("No telemetry records found.")
        return None
    
    return telemetry_storage[-1]

def get_telemetry_stats() -> dict:
    """
    Calculate basic statistics for all stored telemetry records.
    """

    total_packets = len(telemetry_storage)

    normal = 0
    warning = 0
    critical = 0

    for record in telemetry_storage:
        severity = record["analysis"]["severity"]

        if severity == "normal":
            normal += 1

        elif severity == "warning":
            warning += 1

        elif severity == "critical":
            critical += 1

    anomalies = warning + critical

    return {
        "total_packets": total_packets,
        "normal": normal,
        "warning": warning,
        "critical": critical,
        "anomalies": anomalies
    }

def get_health_metrics() -> dict:
    """
    Calculate engineering metrics from all stored telemetry records.
    """

    if not telemetry_storage:
        return {
            "battery": {},
            "temperature": {},
            "cpu": {},
            "signal": {}
        }

    batteries = []
    temperatures = []
    cpu_loads = []
    signal_strengths = []

    for record in telemetry_storage:

        telemetry = record["telemetry"]

        batteries.append(telemetry.battery)
        temperatures.append(telemetry.temperature)
        cpu_loads.append(telemetry.cpu_load)
        signal_strengths.append(telemetry.signal_strength)

    return {
        "battery": {
            "average": round(sum(batteries) / len(batteries), 2),
            "minimum": min(batteries),
            "maximum": max(batteries)
        },

        "temperature": {
            "average": round(sum(temperatures) / len(temperatures), 2),
            "minimum": min(temperatures),
            "maximum": max(temperatures)
        },

        "cpu": {
            "average": round(sum(cpu_loads) / len(cpu_loads), 2),
            "minimum": min(cpu_loads),
            "maximum": max(cpu_loads)
        },

        "signal": {
            "average": round(sum(signal_strengths) / len(signal_strengths), 2),
            "minimum": min(signal_strengths),
            "maximum": max(signal_strengths)
        }
    }

def get_time_statistics() -> dict:
    """
    Calculate time-based statistics for the telemetry mission.
    """

    if not telemetry_storage:
        return {
            "first_packet": None,
            "last_packet": None,
            "mission_duration_seconds": 0,
            "packets": 0,
            "average_interval_seconds": 0,
            "packets_per_minute": 0,
            "packets_per_hour": 0
        }

    timestamps = []

    for record in telemetry_storage:
        timestamps.append(record["telemetry"].timestamp)

    first_packet = timestamps[0]
    last_packet = timestamps[-1]

    packet_count = len(timestamps)

    mission_duration = (
        last_packet - first_packet
    ).total_seconds()

    # Prevent division by zero
    if mission_duration <= 0:
        average_interval = 0
        packets_per_minute = 0
        packets_per_hour = 0

    else:
        average_interval = mission_duration / (packet_count - 1) \
            if packet_count > 1 else 0

        packets_per_minute = packet_count / (mission_duration / 60)

        packets_per_hour = packet_count / (mission_duration / 3600)

    return {
        "first_packet": first_packet.isoformat(),
        "last_packet": last_packet.isoformat(),
        "mission_duration_seconds": round(mission_duration, 2),
        "packets": packet_count,
        "average_interval_seconds": round(average_interval, 2),
        "packets_per_minute": round(packets_per_minute, 2),
        "packets_per_hour": round(packets_per_hour, 2)
    }

def get_mission_summary() -> dict:
    """
    Return a complete mission summary for dashboard use.
    """

    latest = get_latest_telemetry()
    anomalies = get_anomalies()

    return {
        "statistics": get_telemetry_stats(),

        "metrics": get_health_metrics(),

        "time": get_time_statistics(),

        "latest": latest,

        "anomalies": len(anomalies)
    }

def get_dashboard_data() -> dict:
    """
    Return all information required by the frontend dashboard
    in a single request.
    """

    latest = get_latest_telemetry()

    statistics = get_telemetry_stats()

    recent_alerts = get_recent_anomalies(limit=10)

    total_alerts = len(get_anomalies())

    # -------------------------
    # Determine mission status
    # -------------------------

    if statistics["critical"] > 0:
        mission_status = "Critical"

    elif statistics["warning"] > 0:
        mission_status = "Warning"

    else:
        mission_status = "Healthy"

    return {

        "mission_status": mission_status,

        "latest": latest,

        "statistics": statistics,

        "metrics": get_health_metrics(),

        "time": get_time_statistics(),

        "trends": get_trend_analysis(),

        "alerts": recent_alerts,

        "alert_count": total_alerts
    }

def get_trend_analysis() -> dict:
    """
    Analyze engineering trends by comparing the first and latest
    telemetry packets.
    """

    if len(telemetry_storage) < 2:
        return {
            "message": "At least two telemetry packets are required."
        }

    first = telemetry_storage[0]["telemetry"]
    latest = telemetry_storage[-1]["telemetry"]

    def calculate_trend(first_value, latest_value):

        if latest_value > first_value:
            return "increasing"

        elif latest_value < first_value:
            return "decreasing"

        return "stable"

    return {
        "battery": {
            "first": first.battery,
            "latest": latest.battery,
            "trend": calculate_trend(
                first.battery,
                latest.battery
            )
        },

        "temperature": {
            "first": first.temperature,
            "latest": latest.temperature,
            "trend": calculate_trend(
                first.temperature,
                latest.temperature
            )
        },

        "cpu": {
            "first": first.cpu_load,
            "latest": latest.cpu_load,
            "trend": calculate_trend(
                first.cpu_load,
                latest.cpu_load
            )
        },

        "signal": {
            "first": first.signal_strength,
            "latest": latest.signal_strength,
            "trend": calculate_trend(
                first.signal_strength,
                latest.signal_strength
            )
        }
    }

def get_anomalies() -> list[dict]:
    """
    Return every telemetry record that contains an anomaly.
    """

    anomalies = []

    for record in telemetry_storage:
        if record["analysis"]["is_anomaly"]:
            anomalies.append(record)

    return anomalies

def get_recent_anomalies(limit: int = 10) -> list[dict]:
    """
    Return the most recent anomaly records.

    Parameters
    ----------
    limit : int
        Maximum number of anomalies to return.

    Returns
    -------
    list[dict]
        Most recent anomaly records.
    """

    anomalies = get_anomalies()

    return anomalies[-limit:]

def get_telemetry_by_severity(level: str) -> list[dict]:
    """
    Return all telemetry records with the specified severity.
    """

    level = level.lower()

    matching_records = []

    for record in telemetry_storage:
        severity = record["analysis"]["severity"]

        if severity == level:
            matching_records.append(record)

    return matching_records

def get_telemetry_by_satellite(satellite_id: str) -> list[dict]:
    """
    Return all telemetry records for a specific satellite.
    """

    matching_records = []

    for record in telemetry_storage:
        current_id = record["telemetry"].satellite_id

        if current_id == satellite_id:
            matching_records.append(record)

    return matching_records

def search_telemetry(
    satellite_id: str | None = None,
    severity: str | None = None
) -> list[dict]:
    """
    Search telemetry records using optional filters.

    Parameters
    ----------
    satellite_id : str | None
        Filter by satellite ID.

    severity : str | None
        Filter by severity (normal, warning, critical).

    Returns
    -------
    list[dict]
        Matching telemetry records.
    """

    results = []

    for record in telemetry_storage:

        telemetry = record["telemetry"]
        analysis = record["analysis"]

        # -------------------------
        # Satellite filter
        # -------------------------
        if satellite_id is not None:
            if telemetry.satellite_id != satellite_id:
                continue

        # -------------------------
        # Severity filter
        # -------------------------
        if severity is not None:
            if analysis["severity"] != severity.lower():
                continue

        results.append(record)

    return results

