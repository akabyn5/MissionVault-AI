from app.schemas.telemetry import Telemetry


def analyze_telemetry(data: Telemetry) -> dict:
    """
    Analyze a telemetry packet and determine whether it contains
    warning or critical anomalies.

    Returns
    -------
    dict
        {
            "is_anomaly": bool,
            "severity": "normal" | "warning" | "critical",
            "alerts": list[str]
        }
    """

    alerts: list[str] = []

    severity = "normal"

    # -------------------------
    # Battery
    # -------------------------
    if data.battery < 20:
        severity = "critical"
        alerts.append("Battery level is CRITICAL (<20%).")

    elif data.battery <= 40:
        if severity != "critical":
            severity = "warning"
        alerts.append("Battery level is LOW (20-40%).")

    # -------------------------
    # Temperature
    # -------------------------
    if data.temperature > 80:
        severity = "critical"
        alerts.append("Temperature exceeds 80°C.")

    elif data.temperature >= 60:
        if severity != "critical":
            severity = "warning"
        alerts.append("Temperature is elevated (60-80°C).")

    # -------------------------
    # Signal Strength
    # -------------------------
    if data.signal_strength < -100:
        severity = "critical"
        alerts.append("Signal strength is CRITICAL (< -100 dBm).")

    elif data.signal_strength <= -90:
        if severity != "critical":
            severity = "warning"
        alerts.append("Signal strength is weak (-90 to -100 dBm).")

    # -------------------------
    # CPU Load
    # -------------------------
    if data.cpu_load > 95:
        severity = "critical"
        alerts.append("CPU load exceeds 95%.")

    elif data.cpu_load >= 80:
        if severity != "critical":
            severity = "warning"
        alerts.append("CPU load is high (80-95%).")

    # -------------------------
    # Payload Status
    # -------------------------
    if data.payload_status.upper() == "ERROR":
        severity = "critical"
        alerts.append("Payload status is ERROR.")

    return {
        "is_anomaly": len(alerts) > 0,
        "severity": severity,
        "alerts": alerts
    }