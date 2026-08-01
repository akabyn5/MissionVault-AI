export default function AlertsCard({ alerts }) {

    return (

        <div>

            <h2>Recent Alerts</h2>

            {alerts.length === 0 ? (

                <p>No alerts.</p>

            ) : (

                alerts.map((alert, index) => (

                    <div key={index}>

                        <strong>

                            {alert.analysis.severity.toUpperCase()}

                        </strong>

                        <ul>

                            {alert.analysis.alerts.map((message, i) => (

                                <li key={i}>{message}</li>

                            ))}

                        </ul>

                    </div>

                ))

            )}

        </div>

    );

}