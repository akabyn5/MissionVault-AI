export default function MissionStatusCard({ status }) {

    const normalizedStatus = status?.toLowerCase() || "unknown";

    const statusLabels = {
        healthy: "Healthy",
        warning: "Warning",
        critical: "Critical",
        unknown: "Unknown"
    };

    const displayStatus =
        statusLabels[normalizedStatus] || "Unknown";

    return (
        <section className={`mission-status-card status-${normalizedStatus}`}>

            <div className="mission-status-header">
                <h2>Mission Status</h2>

                <span
                    className="mission-status-indicator"
                    aria-label={`Mission status: ${displayStatus}`}
                />
            </div>

            <p className="mission-status-value">
                {displayStatus}
            </p>

        </section>
    );
}