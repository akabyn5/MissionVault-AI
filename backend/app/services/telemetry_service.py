import json
import logging
from datetime import datetime, timezone

from sqlalchemy import func
from sqlalchemy import select

from app.database.database import SessionLocal
from app.models.telemetry import TelemetryRecord
from app.schemas.telemetry import Telemetry


# ---------------------------------------------------------
# Logging
# ---------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def _serialize_record(record: TelemetryRecord) -> dict:
    """
    Convert a database record into the same dictionary
    structure used by the existing API.

    This preserves compatibility with the frontend.
    """

    return {
        "telemetry": {
            "satellite_id": record.satellite_id,
            "battery": record.battery,
            "temperature": record.temperature,
            "signal_strength": record.signal_strength,
            "cpu_load": record.cpu_load,
            "payload_status": record.payload_status,
            "timestamp": record.timestamp
        },

        "analysis": {
            "is_anomaly": record.is_anomaly,
            "severity": record.severity,
            "alerts": json.loads(
                record.alerts or "[]"
            )
        }
    }


def _parse_timestamp(timestamp: str) -> datetime:
    """
    Convert an ISO 8601 timestamp string into a datetime object.
    """

    parsed = datetime.fromisoformat(timestamp)

    if parsed.tzinfo is None:
        parsed = parsed.replace(
            tzinfo=timezone.utc
        )

    return parsed


# ---------------------------------------------------------
# Save telemetry
# ---------------------------------------------------------

def save_telemetry(
    data: Telemetry,
    analysis: dict
) -> dict:
    """
    Persist a telemetry packet and its analysis
    into the SQLite database.
    """

    record = TelemetryRecord(
        satellite_id=data.satellite_id,
        battery=data.battery,
        temperature=data.temperature,
        signal_strength=data.signal_strength,
        cpu_load=data.cpu_load,
        payload_status=data.payload_status,
        timestamp=data.timestamp.isoformat(),

        is_anomaly=analysis.get(
            "is_anomaly",
            False
        ),

        severity=analysis.get(
            "severity",
            "normal"
        ),

        alerts=json.dumps(
            analysis.get(
                "alerts",
                []
            )
        )
    )

    with SessionLocal() as db:

        db.add(record)

        db.commit()

        db.refresh(record)

        logger.info(
            "Stored telemetry packet ID: %d",
            record.id
        )

        logger.info(
            "Total stored packets: %d",
            db.scalar(
                select(
                    func.count(
                        TelemetryRecord.id
                    )
                )
            )
        )

        return _serialize_record(
            record
        )


# ---------------------------------------------------------
# Get all telemetry
# ---------------------------------------------------------

def get_all_telemetry() -> list[dict]:
    """
    Return all telemetry records ordered by insertion order.
    """

    with SessionLocal() as db:

        statement = (
            select(TelemetryRecord)
            .order_by(
                TelemetryRecord.id.asc()
            )
        )

        records = db.scalars(
            statement
        ).all()

        return [
            _serialize_record(record)
            for record in records
        ]


# ---------------------------------------------------------
# Get latest telemetry
# ---------------------------------------------------------

def get_latest_telemetry() -> dict | None:
    """
    Return the most recently stored telemetry record.
    """

    with SessionLocal() as db:

        statement = (
            select(TelemetryRecord)
            .order_by(
                TelemetryRecord.id.desc()
            )
            .limit(1)
        )

        record = db.scalars(
            statement
        ).first()

        if record is None:

            logger.warning(
                "No telemetry records found."
            )

            return None

        return _serialize_record(
            record
        )


# ---------------------------------------------------------
# Current mission status
# ---------------------------------------------------------

def get_current_mission_status() -> str:
    """
    Determine the current mission status using only
    the latest telemetry packet.

    Historical statistics do not determine current status.
    """

    latest = get_latest_telemetry()

    if latest is None:
        return "Unknown"

    severity = latest["analysis"].get(
        "severity",
        "normal"
    ).lower()

    if severity == "critical":
        return "Critical"

    if severity == "warning":
        return "Warning"

    return "Healthy"


# ---------------------------------------------------------
# Historical telemetry statistics
# ---------------------------------------------------------

def get_telemetry_stats() -> dict:
    """
    Calculate historical statistics from persistent telemetry.
    """

    with SessionLocal() as db:

        total_packets = db.scalar(
            select(
                func.count(
                    TelemetryRecord.id
                )
            )
        ) or 0

        normal = db.scalar(
            select(
                func.count(
                    TelemetryRecord.id
                )
            ).where(
                TelemetryRecord.severity == "normal"
            )
        ) or 0

        warning = db.scalar(
            select(
                func.count(
                    TelemetryRecord.id
                )
            ).where(
                TelemetryRecord.severity == "warning"
            )
        ) or 0

        critical = db.scalar(
            select(
                func.count(
                    TelemetryRecord.id
                )
            ).where(
                TelemetryRecord.severity == "critical"
            )
        ) or 0

        anomalies = warning + critical

        return {
            "total_packets": total_packets,
            "normal": normal,
            "warning": warning,
            "critical": critical,
            "anomalies": anomalies
        }


# ---------------------------------------------------------
# Engineering health metrics
# ---------------------------------------------------------

def get_health_metrics() -> dict:
    """
    Calculate engineering metrics directly from the database.
    """

    with SessionLocal() as db:

        total_packets = db.scalar(
            select(
                func.count(
                    TelemetryRecord.id
                )
            )
        ) or 0

        if total_packets == 0:

            return {
                "battery": {},
                "temperature": {},
                "cpu": {},
                "signal": {}
            }

        battery_stats = db.execute(
            select(
                func.avg(
                    TelemetryRecord.battery
                ),
                func.min(
                    TelemetryRecord.battery
                ),
                func.max(
                    TelemetryRecord.battery
                )
            )
        ).one()

        temperature_stats = db.execute(
            select(
                func.avg(
                    TelemetryRecord.temperature
                ),
                func.min(
                    TelemetryRecord.temperature
                ),
                func.max(
                    TelemetryRecord.temperature
                )
            )
        ).one()

        cpu_stats = db.execute(
            select(
                func.avg(
                    TelemetryRecord.cpu_load
                ),
                func.min(
                    TelemetryRecord.cpu_load
                ),
                func.max(
                    TelemetryRecord.cpu_load
                )
            )
        ).one()

        signal_stats = db.execute(
            select(
                func.avg(
                    TelemetryRecord.signal_strength
                ),
                func.min(
                    TelemetryRecord.signal_strength
                ),
                func.max(
                    TelemetryRecord.signal_strength
                )
            )
        ).one()

        return {
            "battery": {
                "average": round(
                    battery_stats[0],
                    2
                ),
                "minimum": battery_stats[1],
                "maximum": battery_stats[2]
            },

            "temperature": {
                "average": round(
                    temperature_stats[0],
                    2
                ),
                "minimum": temperature_stats[1],
                "maximum": temperature_stats[2]
            },

            "cpu": {
                "average": round(
                    cpu_stats[0],
                    2
                ),
                "minimum": cpu_stats[1],
                "maximum": cpu_stats[2]
            },

            "signal": {
                "average": round(
                    signal_stats[0],
                    2
                ),
                "minimum": signal_stats[1],
                "maximum": signal_stats[2]
            }
        }


# ---------------------------------------------------------
# Time statistics
# ---------------------------------------------------------

def get_time_statistics() -> dict:
    """
    Calculate time-based mission statistics.
    """

    with SessionLocal() as db:

        packet_count = db.scalar(
            select(
                func.count(
                    TelemetryRecord.id
                )
            )
        ) or 0

        if packet_count == 0:

            return {
                "first_packet": None,
                "last_packet": None,
                "mission_duration_seconds": 0,
                "packets": 0,
                "average_interval_seconds": 0,
                "packets_per_minute": 0,
                "packets_per_hour": 0
            }

        first_statement = (
            select(TelemetryRecord)
            .order_by(
                TelemetryRecord.id.asc()
            )
            .limit(1)
        )

        last_statement = (
            select(TelemetryRecord)
            .order_by(
                TelemetryRecord.id.desc()
            )
            .limit(1)
        )

        first_record = db.scalars(
            first_statement
        ).first()

        last_record = db.scalars(
            last_statement
        ).first()

        first_packet = _parse_timestamp(
            first_record.timestamp
        )

        last_packet = _parse_timestamp(
            last_record.timestamp
        )

        mission_duration = (
            last_packet - first_packet
        ).total_seconds()

        if mission_duration <= 0:

            average_interval = 0
            packets_per_minute = 0
            packets_per_hour = 0

        else:

            average_interval = (
                mission_duration
                / (packet_count - 1)
                if packet_count > 1
                else 0
            )

            packets_per_minute = (
                packet_count
                / (mission_duration / 60)
            )

            packets_per_hour = (
                packet_count
                / (mission_duration / 3600)
            )

        return {
            "first_packet": first_record.timestamp,
            "last_packet": last_record.timestamp,

            "mission_duration_seconds": round(
                mission_duration,
                2
            ),

            "packets": packet_count,

            "average_interval_seconds": round(
                average_interval,
                2
            ),

            "packets_per_minute": round(
                packets_per_minute,
                2
            ),

            "packets_per_hour": round(
                packets_per_hour,
                2
            )
        }


# ---------------------------------------------------------
# Mission summary
# ---------------------------------------------------------

def get_mission_summary() -> dict:
    """
    Return a complete mission summary.
    """

    latest = get_latest_telemetry()

    statistics = get_telemetry_stats()

    return {
        "statistics": statistics,

        "metrics": get_health_metrics(),

        "time": get_time_statistics(),

        "latest": latest,

        "anomalies": statistics["anomalies"]
    }


# ---------------------------------------------------------
# Trend analysis
# ---------------------------------------------------------

def get_trend_analysis() -> dict:
    """
    Analyze engineering trends using the first and latest
    persistent telemetry packets.
    """

    with SessionLocal() as db:

        first_statement = (
            select(TelemetryRecord)
            .order_by(
                TelemetryRecord.id.asc()
            )
            .limit(1)
        )

        last_statement = (
            select(TelemetryRecord)
            .order_by(
                TelemetryRecord.id.desc()
            )
            .limit(1)
        )

        first = db.scalars(
            first_statement
        ).first()

        latest = db.scalars(
            last_statement
        ).first()

        if first is None or latest is None:

            return {
                "message": (
                    "At least two telemetry packets "
                    "are required."
                )
            }

        if first.id == latest.id:

            return {
                "message": (
                    "At least two telemetry packets "
                    "are required."
                )
            }

        def calculate_trend(
            first_value,
            latest_value
        ):

            if latest_value > first_value:
                return "increasing"

            if latest_value < first_value:
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


# ---------------------------------------------------------
# All anomalies
# ---------------------------------------------------------

def get_anomalies() -> list[dict]:
    """
    Return every telemetry record containing an anomaly.
    """

    with SessionLocal() as db:

        statement = (
            select(TelemetryRecord)
            .where(
                TelemetryRecord.is_anomaly.is_(True)
            )
            .order_by(
                TelemetryRecord.id.asc()
            )
        )

        records = db.scalars(
            statement
        ).all()

        return [
            _serialize_record(record)
            for record in records
        ]


# ---------------------------------------------------------
# Recent anomalies
# ---------------------------------------------------------

def get_recent_anomalies(
    limit: int = 10
) -> list[dict]:
    """
    Return the most recent anomaly records.

    The result is returned in oldest-to-newest order
    so the frontend can reverse it for display.
    """

    if limit <= 0:
        return []

    with SessionLocal() as db:

        statement = (
            select(TelemetryRecord)
            .where(
                TelemetryRecord.is_anomaly.is_(True)
            )
            .order_by(
                TelemetryRecord.id.desc()
            )
            .limit(limit)
        )

        records = db.scalars(
            statement
        ).all()

        records = list(
            reversed(records)
        )

        return [
            _serialize_record(record)
            for record in records
        ]


# ---------------------------------------------------------
# Filter by severity
# ---------------------------------------------------------

def get_telemetry_by_severity(
    level: str
) -> list[dict]:
    """
    Return telemetry records for a specific severity.
    """

    level = level.lower()

    with SessionLocal() as db:

        statement = (
            select(TelemetryRecord)
            .where(
                TelemetryRecord.severity == level
            )
            .order_by(
                TelemetryRecord.id.asc()
            )
        )

        records = db.scalars(
            statement
        ).all()

        return [
            _serialize_record(record)
            for record in records
        ]


# ---------------------------------------------------------
# Filter by satellite
# ---------------------------------------------------------

def get_telemetry_by_satellite(
    satellite_id: str
) -> list[dict]:
    """
    Return all telemetry records for a satellite.
    """

    with SessionLocal() as db:

        statement = (
            select(TelemetryRecord)
            .where(
                TelemetryRecord.satellite_id
                == satellite_id
            )
            .order_by(
                TelemetryRecord.id.asc()
            )
        )

        records = db.scalars(
            statement
        ).all()

        return [
            _serialize_record(record)
            for record in records
        ]


# ---------------------------------------------------------
# Search telemetry
# ---------------------------------------------------------

def search_telemetry(
    satellite_id: str | None = None,
    severity: str | None = None
) -> list[dict]:
    """
    Search persistent telemetry records
    using optional filters.
    """

    with SessionLocal() as db:

        statement = select(
            TelemetryRecord
        )

        if satellite_id is not None:

            statement = statement.where(
                TelemetryRecord.satellite_id
                == satellite_id
            )

        if severity is not None:

            statement = statement.where(
                TelemetryRecord.severity
                == severity.lower()
            )

        statement = statement.order_by(
            TelemetryRecord.id.asc()
        )

        records = db.scalars(
            statement
        ).all()

        return [
            _serialize_record(record)
            for record in records
        ]


# ---------------------------------------------------------
# Dashboard data
# ---------------------------------------------------------

def get_dashboard_data() -> dict:
    """
    Return all information required by the frontend
    dashboard in a single request.

    The frontend does not need to know whether the
    data comes from memory or persistent storage.
    """

    latest = get_latest_telemetry()

    statistics = get_telemetry_stats()

    recent_alerts = get_recent_anomalies(
        limit=10
    )

    mission_status = (
        get_current_mission_status()
    )

    return {

        # Current mission state
        "mission_status": mission_status,

        # Most recent telemetry
        "latest": latest,

        # Historical statistics
        "statistics": statistics,

        # Engineering metrics
        "metrics": get_health_metrics(),

        # Time statistics
        "time": get_time_statistics(),

        # Long-term trends
        "trends": get_trend_analysis(),

        # Recent anomalies only
        "alerts": recent_alerts,

        # Total historical anomaly count
        "alert_count": statistics["anomalies"]
    }