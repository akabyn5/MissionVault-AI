# backend/app/database/migrate.py
from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine


def ensure_telemetry_midnight_columns(engine: Engine) -> None:
    """
    Add Midnight columns to telemetry_records if they are missing.

    Safe for SQLite. Existing rows get defaults where needed.
    """
    inspector = inspect(engine)

    if "telemetry_records" not in inspector.get_table_names():
        return

    existing_columns = {col["name"] for col in inspector.get_columns("telemetry_records")}

    statements = []

    if "midnight_enabled" not in existing_columns:
        statements.append(
            "ALTER TABLE telemetry_records ADD COLUMN midnight_enabled BOOLEAN NOT NULL DEFAULT 0"
        )

    if "midnight_status" not in existing_columns:
        statements.append(
            "ALTER TABLE telemetry_records ADD COLUMN midnight_status VARCHAR NOT NULL DEFAULT 'local-only'"
        )

    if "midnight_network" not in existing_columns:
        statements.append(
            "ALTER TABLE telemetry_records ADD COLUMN midnight_network VARCHAR NULL"
        )

    if "midnight_contract_address" not in existing_columns:
        statements.append(
            "ALTER TABLE telemetry_records ADD COLUMN midnight_contract_address VARCHAR NULL"
        )

    if "midnight_commitment" not in existing_columns:
        statements.append(
            "ALTER TABLE telemetry_records ADD COLUMN midnight_commitment VARCHAR NULL"
        )

    if "midnight_tx_hash" not in existing_columns:
        statements.append(
            "ALTER TABLE telemetry_records ADD COLUMN midnight_tx_hash VARCHAR NULL"
        )

    if "midnight_anchored_at" not in existing_columns:
        statements.append(
            "ALTER TABLE telemetry_records ADD COLUMN midnight_anchored_at VARCHAR NULL"
        )

    if "midnight_error" not in existing_columns:
        statements.append(
            "ALTER TABLE telemetry_records ADD COLUMN midnight_error TEXT NULL"
        )

    if not statements:
        return

    with engine.begin() as conn:
        for stmt in statements:
            conn.execute(text(stmt))