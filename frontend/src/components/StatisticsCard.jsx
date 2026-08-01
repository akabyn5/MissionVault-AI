export default function StatisticsCard({ statistics }) {

    return (

        <div>

            <h2>Statistics</h2>

            <p>Total Packets: {statistics.total_packets}</p>

            <p>Normal: {statistics.normal}</p>

            <p>Warning: {statistics.warning}</p>

            <p>Critical: {statistics.critical}</p>

            <p>Anomalies: {statistics.anomalies}</p>

        </div>

    );

}