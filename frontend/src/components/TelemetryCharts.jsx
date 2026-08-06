import { Line } from "react-chartjs-2";
import "chart.js/auto";

function formatUtcTime(timestamp) {

    if (!timestamp) {
        return "Unknown";
    }

    const date = new Date(timestamp);

    if (Number.isNaN(date.getTime())) {
        return "Invalid";
    }

    return date.toLocaleTimeString(
        "en-GB",
        {
            timeZone: "UTC",
            hour: "2-digit",
            minute: "2-digit",
            second: "2-digit",
            hour12: false
        }
    );
}


function createChartData(
    history,
    label,
    field,
    borderColor,
    backgroundColor
) {

    return {

        labels: history.map(
            (point) =>
                formatUtcTime(
                    point.timestamp
                )
        ),

        datasets: [

            {
                label: label,

                data: history.map(
                    (point) =>
                        point[field]
                ),

                borderColor: borderColor,

                backgroundColor: backgroundColor,

                borderWidth: 2,

                pointRadius: 2,

                pointHoverRadius: 5,

                tension: 0.25,

                fill: true
            }

        ]
    };
}


function createChartOptions(
    yAxisTitle
) {

    return {

        responsive: true,

        maintainAspectRatio: false,

        interaction: {

            mode: "index",

            intersect: false
        },

        plugins: {

            legend: {

                display: false
            },

            tooltip: {

                callbacks: {

                    title: function (
                        tooltipItems
                    ) {

                        if (
                            !tooltipItems.length
                        ) {

                            return "";
                        }

                        return (
                            tooltipItems[0]
                                .label
                            + " UTC"
                        );
                    }

                }
            }

        },

        scales: {

            x: {

                ticks: {

                    maxTicksLimit: 8,

                    maxRotation: 0
                },

                grid: {

                    display: false
                }

            },

            y: {

                title: {

                    display: true,

                    text: yAxisTitle
                },

                beginAtZero: false
            }

        }

    };
}


function ChartCard({
    title,
    history,
    field,
    unit,
    borderColor,
    backgroundColor
}) {

    const chartData = createChartData(
        history,
        title,
        field,
        borderColor,
        backgroundColor
    );

    const chartOptions =
        createChartOptions(
            unit
        );

    return (

        <article className="telemetry-chart-card">

            <div className="telemetry-chart-header">

                <h3>
                    {title}
                </h3>

                <span>
                    {history.length} samples
                </span>

            </div>

            <div className="telemetry-chart-container">

                <Line
                    data={chartData}
                    options={chartOptions}
                />

            </div>

        </article>

    );
}


export default function TelemetryCharts({
    history
}) {

    const safeHistory =
        Array.isArray(history)
            ? history
            : [];

    if (
        safeHistory.length === 0
    ) {

        return (

            <section className="telemetry-charts-section">

                <div className="telemetry-charts-header">

                    <div>

                        <h2>
                            Telemetry Visualization
                        </h2>

                        <p>
                            Waiting for historical
                            telemetry data...
                        </p>

                    </div>

                </div>

            </section>
        );
    }


    return (

        <section className="telemetry-charts-section">

            <div className="telemetry-charts-header">

                <div>

                    <h2>
                        Telemetry Visualization
                    </h2>

                    <p>
                        Recent satellite telemetry
                        trends from persistent mission data.
                    </p>

                </div>

                <span className="telemetry-chart-count">

                    {safeHistory.length}

                </span>

            </div>


            <div className="telemetry-charts-grid">

                <ChartCard

                    title="Battery Level"

                    history={safeHistory}

                    field="battery"

                    unit="Battery (%)"

                    borderColor="#22d3ee"

                    backgroundColor="rgba(34, 211, 238, 0.10)"

                />


                <ChartCard

                    title="Temperature"

                    history={safeHistory}

                    field="temperature"

                    unit="Temperature (°C)"

                    borderColor="#f59e0b"

                    backgroundColor="rgba(245, 158, 11, 0.10)"

                />


                <ChartCard

                    title="CPU Load"

                    history={safeHistory}

                    field="cpu_load"

                    unit="CPU Load (%)"

                    borderColor="#a78bfa"

                    backgroundColor="rgba(167, 139, 250, 0.10)"

                />


                <ChartCard

                    title="Signal Strength"

                    history={safeHistory}

                    field="signal_strength"

                    unit="Signal (dBm)"

                    borderColor="#60a5fa"

                    backgroundColor="rgba(96, 165, 250, 0.10)"

                />

            </div>

        </section>

    );

}