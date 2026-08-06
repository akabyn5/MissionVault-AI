function formatUtcTime(timestamp) {

    if (!timestamp) {
        return "Unknown";
    }


    const date = new Date(
        timestamp
    );


    if (
        Number.isNaN(
            date.getTime()
        )
    ) {

        return "Invalid";

    }


    return date.toLocaleString(
        "en-GB",
        {
            timeZone: "UTC",

            year: "numeric",

            month: "2-digit",

            day: "2-digit",

            hour: "2-digit",

            minute: "2-digit",

            second: "2-digit",

            hour12: false
        }
    ) + " UTC";

}


function getSeverityClass(
    severity
) {

    const normalizedSeverity =
        severity?.toLowerCase()
        || "unknown";


    return (
        `search-severity-${normalizedSeverity}`
    );

}


export default function SearchResultsCard({
    results,
    loading,
    error,
    activeFilters
}) {

    const safeResults =
        Array.isArray(results)
            ? results
            : [];


    return (

        <section className="search-results-section">

            <div className="search-results-header">

                <div>

                    <h2>
                        Search Results
                    </h2>

                    {activeFilters && (

                        <p>

                            Showing the most recent
                            matching telemetry records.

                        </p>

                    )}

                </div>


                <span className="search-results-count">

                    {safeResults.length}

                </span>

            </div>


            {loading && (

                <div className="search-results-state">

                    <p>
                        Searching telemetry database...
                    </p>

                </div>

            )}


            {!loading && error && (

                <div className="search-results-error">

                    <strong>
                        Search failed
                    </strong>

                    <p>
                        {error}
                    </p>

                </div>

            )}


            {!loading &&
                !error &&
                !activeFilters && (

                <div className="search-results-state">

                    <p>
                        Apply a filter to search
                        persistent telemetry.
                    </p>

                </div>

            )}


            {!loading &&
                !error &&
                activeFilters &&
                safeResults.length === 0 && (

                <div className="search-results-state">

                    <p>
                        No telemetry records matched
                        the selected filters.
                    </p>

                </div>

            )}


            {!loading &&
                !error &&
                activeFilters &&
                safeResults.length > 0 && (

                <div className="search-results-table-wrapper">

                    <table className="search-results-table">

                        <thead>

                            <tr>

                                <th>
                                    Time
                                </th>

                                <th>
                                    Satellite
                                </th>

                                <th>
                                    Severity
                                </th>

                                <th>
                                    Battery
                                </th>

                                <th>
                                    Temperature
                                </th>

                                <th>
                                    CPU
                                </th>

                                <th>
                                    Signal
                                </th>

                                <th>
                                    Payload
                                </th>

                            </tr>

                        </thead>


                        <tbody>

                            {safeResults.map(
                                (record, index) => {

                                    const telemetry =
                                        record?.telemetry
                                        || {};

                                    const analysis =
                                        record?.analysis
                                        || {};

                                    const severity =
                                        analysis.severity
                                        || "unknown";


                                    return (

                                        <tr
                                            key={
                                                `${telemetry.timestamp || "record"}-${index}`
                                            }
                                        >

                                            <td>

                                                {formatUtcTime(
                                                    telemetry.timestamp
                                                )}

                                            </td>


                                            <td>

                                                <strong>
                                                    {
                                                        telemetry.satellite_id
                                                        || "Unknown"
                                                    }
                                                </strong>

                                            </td>


                                            <td>

                                                <span
                                                    className={
                                                        `search-severity-badge ` +
                                                        getSeverityClass(
                                                            severity
                                                        )
                                                    }
                                                >
                                                    {
                                                        severity.toUpperCase()
                                                    }
                                                </span>

                                            </td>


                                            <td>

                                                {
                                                    telemetry.battery
                                                    ?? "-"
                                                }%

                                            </td>


                                            <td>

                                                {
                                                    telemetry.temperature
                                                    ?? "-"
                                                } °C

                                            </td>


                                            <td>

                                                {
                                                    telemetry.cpu_load
                                                    ?? "-"
                                                }%

                                            </td>


                                            <td>

                                                {
                                                    telemetry.signal_strength
                                                    ?? "-"
                                                } dBm

                                            </td>


                                            <td>

                                                {
                                                    telemetry.payload_status
                                                    || "-"
                                                }

                                            </td>

                                        </tr>

                                    );

                                }
                            )}

                        </tbody>

                    </table>

                </div>

            )}

        </section>

    );

}