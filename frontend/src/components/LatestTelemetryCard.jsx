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

    return (
        <div>

            <h2>Latest Telemetry</h2>

            <p>Satellite: {telemetry.satellite_id}</p>

            <p>Battery: {telemetry.battery}%</p>

            <p>Temperature: {telemetry.temperature} °C</p>

            <p>CPU: {telemetry.cpu_load}%</p>

            <p>Signal: {telemetry.signal_strength} dBm</p>

            <p>Status: {telemetry.payload_status}</p>

        </div>
    );
}