from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text

from app.database.database import Base


class TelemetryRecord(Base):
    """
    Persistent database model for satellite telemetry.

    This table stores both:
    - Raw telemetry values
    - Telemetry analysis results
    """

    __tablename__ = "telemetry_records"

    # -----------------------------------------------------
    # Primary key
    # -----------------------------------------------------

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    # -----------------------------------------------------
    # Telemetry data
    # -----------------------------------------------------

    satellite_id = Column(
        String,
        nullable=False,
        index=True
    )

    battery = Column(
        Float,
        nullable=False
    )

    temperature = Column(
        Float,
        nullable=False
    )

    signal_strength = Column(
        Integer,
        nullable=False
    )

    cpu_load = Column(
        Float,
        nullable=False
    )

    payload_status = Column(
        String,
        nullable=False
    )

    # ISO 8601 timestamp stored as text.
    # This preserves timezone information exactly
    # as received from the telemetry simulator.
    timestamp = Column(
        String,
        nullable=False,
        index=True
    )

    # -----------------------------------------------------
    # Analysis data
    # -----------------------------------------------------

    is_anomaly = Column(
        Boolean,
        nullable=False,
        default=False,
        index=True
    )

    severity = Column(
        String,
        nullable=False,
        default="normal",
        index=True
    )

    # JSON-encoded list of alert messages.
    #
    # Example:
    # [
    #   "Battery level is CRITICAL (<20%)."
    # ]
    alerts = Column(
        Text,
        nullable=False,
        default="[]"
    )