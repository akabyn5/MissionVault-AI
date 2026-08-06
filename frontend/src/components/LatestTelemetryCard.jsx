export default function LatestTelemetryCard({ latest }) {
    if (!latest) {
        return (
            <div>
                <h2>Latest Telemetry</h2>
                <p>No telemetry available.</p>
            </div>
        );
    }

    const telemetry = latest.telemetry;
    const midnight = latest.midnight || {};

    return (
        <div>
            <h2>Latest Telemetry</h2>

            <p>Satellite: {telemetry.satellite_id}</p>
            <p>Battery: {telemetry.battery}%</p>
            <p>Temperature: {telemetry.temperature} °C</p>
            <p>CPU: {telemetry.cpu_load}%</p>
            <p>Signal: {telemetry.signal_strength} dBm</p>
            <p>Status: {telemetry.payload_status}</p>

            <h3>Midnight</h3>
            <p>Mode: {midnight.status || "local-only"}</p>
            <p>Network: {midnight.network || "-"}</p>
            <p>Commitment: {midnight.commitment || "-"}</p>
            <p>Tx hash: {midnight.tx_hash || "-"}</p>
            {midnight.error ? <p>Error: {midnight.error}</p> : null}
        </div>
    );
}