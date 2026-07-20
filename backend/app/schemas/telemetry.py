from pydantic import BaseModel
from datetime import datetime


class Telemetry(BaseModel):
    satellite_id: str
    battery: float
    temperature: float
    signal_strength: int
    cpu_load: float
    payload_status: str
    timestamp: datetime