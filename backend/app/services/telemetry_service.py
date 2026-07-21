import logging

from app.schemas.telemetry import Telemetry

# Configure the logger for this module
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)

# Temporary in-memory storage
telemetry_storage: list[Telemetry] = []


def save_telemetry(data: Telemetry) -> Telemetry:
    """
    Store a telemetry packet in temporary memory.
    """

    telemetry_storage.append(data)

    logger.info("Stored packets: %d", len(telemetry_storage))
    logger.info("Latest packet: %s", data)

    return data


def get_all_telemetry() -> list[Telemetry]:
    """
    Return a copy of all stored telemetry packets.
    """

    return telemetry_storage.copy()