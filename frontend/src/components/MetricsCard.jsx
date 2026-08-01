export default function MetricsCard({ metrics }) {

    return (

        <div>

            <h2>Health Metrics</h2>

            <h3>Battery</h3>
            <p>Average: {metrics.battery.average}</p>
            <p>Minimum: {metrics.battery.minimum}</p>
            <p>Maximum: {metrics.battery.maximum}</p>

            <h3>Temperature</h3>
            <p>Average: {metrics.temperature.average}</p>
            <p>Minimum: {metrics.temperature.minimum}</p>
            <p>Maximum: {metrics.temperature.maximum}</p>

            <h3>CPU</h3>
            <p>Average: {metrics.cpu.average}</p>
            <p>Minimum: {metrics.cpu.minimum}</p>
            <p>Maximum: {metrics.cpu.maximum}</p>

            <h3>Signal</h3>
            <p>Average: {metrics.signal.average}</p>
            <p>Minimum: {metrics.signal.minimum}</p>
            <p>Maximum: {metrics.signal.maximum}</p>

        </div>

    );

}