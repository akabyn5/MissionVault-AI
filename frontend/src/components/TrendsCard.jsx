export default function TrendCard({ trends }) {

    if (!trends.battery) {

        return (
            <div>

                <h2>Trends</h2>

                <p>Not enough telemetry.</p>

            </div>
        );

    }

    return (

        <div>

            <h2>Trends</h2>

            <p>Battery: {trends.battery.trend}</p>

            <p>Temperature: {trends.temperature.trend}</p>

            <p>CPU: {trends.cpu.trend}</p>

            <p>Signal: {trends.signal.trend}</p>

        </div>

    );

}