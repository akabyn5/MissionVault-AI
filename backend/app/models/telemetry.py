# backend/app/models/telemetry.py
from sqlalchemy import Boolean, Column, Float, Integer, String, Text

from app.database.database import Base


class TelemetryRecord(Base):
    """
    Persistent database model for satellite telemetry.
    """

    __tablename__ = "telemetry_records"

    id = Column(Integer, primary_key=True, index=True)

    satellite_id = Column(String, nullable=False, index=True)
    battery = Column(Float, nullable=False)
    temperature = Column(Float, nullable=False)
    signal_strength = Column(Integer, nullable=False)
    cpu_load = Column(Float, nullable=False)
    payload_status = Column(String, nullable=False)

    timestamp = Column(String, nullable=False, index=True)

    is_anomaly = Column(Boolean, nullable=False, default=False, index=True)
    severity = Column(String, nullable=False, default="normal", index=True)
    alerts = Column(Text, nullable=False, default="[]")

    # Midnight anchoring fields
    midnight_enabled = Column(Boolean, nullable=False, default=False, index=True)
    midnight_status = Column(String, nullable=False, default="local-only", index=True)
    midnight_network = Column(String, nullable=True)
    midnight_contract_address = Column(String, nullable=True)
    midnight_commitment = Column(String, nullable=True, index=True)
    midnight_tx_hash = Column(String, nullable=True, index=True)
    midnight_anchored_at = Column(String, nullable=True)
    midnight_error = Column(Text, nullable=True)