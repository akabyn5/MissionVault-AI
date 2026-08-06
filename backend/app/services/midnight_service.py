# backend/app/services/midnight_service.py
import hashlib
import json
import logging
import os
from datetime import datetime, timezone

import requests

logger = logging.getLogger(__name__)

MIDNIGHT_ENABLED = os.getenv("MIDNIGHT_ENABLED", "false").lower() == "true"
MIDNIGHT_ANCHOR_URL = os.getenv("MIDNIGHT_ANCHOR_URL", "").strip()
MIDNIGHT_NETWORK = os.getenv("MIDNIGHT_NETWORK", "preprod").strip()
MIDNIGHT_CONTRACT_ADDRESS = os.getenv("MIDNIGHT_CONTRACT_ADDRESS", "").strip()


def build_commitment(payload: dict) -> str:
    """
    Build a stable SHA-256 commitment from a telemetry payload.
    """
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()


def anchor_telemetry(payload: dict) -> dict:
    """
    Prepare and optionally submit a telemetry commitment to a Midnight bridge endpoint.

    This is a safe integration boundary:
    - If MIDNIGHT_ENABLED is false, it stays local-only.
    - If MIDNIGHT_ANCHOR_URL is set, the app posts the commitment to that service.
    """
    commitment = build_commitment(payload)
    anchored_at = datetime.now(timezone.utc).isoformat()

    base_receipt = {
        "enabled": MIDNIGHT_ENABLED,
        "network": MIDNIGHT_NETWORK,
        "contract_address": MIDNIGHT_CONTRACT_ADDRESS or None,
        "commitment": commitment,
        "anchored_at": anchored_at,
        "tx_hash": None,
        "status": "local-only",
        "error": None,
    }

    if not MIDNIGHT_ENABLED or not MIDNIGHT_ANCHOR_URL:
        logger.info("Midnight anchoring disabled. Storing local receipt only.")
        return base_receipt

    try:
        response = requests.post(
            MIDNIGHT_ANCHOR_URL,
            json={
                "network": MIDNIGHT_NETWORK,
                "contract_address": MIDNIGHT_CONTRACT_ADDRESS,
                "commitment": commitment,
                "payload": payload,
            },
            timeout=10
        )

        if not response.ok:
            return {
                **base_receipt,
                "status": "failed",
                "error": f"HTTP {response.status_code}",
            }

        data = response.json() if response.content else {}
        tx_hash = (
            data.get("tx_hash")
            or data.get("transaction_hash")
            or data.get("hash")
        )

        return {
            **base_receipt,
            "status": data.get("status", "anchored"),
            "tx_hash": tx_hash,
        }

    except Exception as error:
        logger.exception("Midnight anchoring failed")
        return {
            **base_receipt,
            "status": "failed",
            "error": str(error),
        }