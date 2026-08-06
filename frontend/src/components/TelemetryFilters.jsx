import { useState } from "react";


export default function TelemetryFilters({
    onApply,
    onClear,
    loading
}) {

    const [
        satelliteId,
        setSatelliteId
    ] = useState("");


    const [
        severity,
        setSeverity
    ] = useState("");


    function handleSubmit(event) {

        event.preventDefault();


        onApply({

            satelliteId:
                satelliteId.trim(),

            severity

        });

    }


    function handleClear() {

        setSatelliteId("");

        setSeverity("");

        onClear();

    }


    return (

        <section className="telemetry-filters-section">

            <div className="telemetry-filters-header">

                <div>

                    <h2>
                        Telemetry Search
                    </h2>

                    <p>
                        Search persistent telemetry
                        by satellite ID and severity.
                    </p>

                </div>

            </div>


            <form
                className="telemetry-filters-form"
                onSubmit={handleSubmit}
            >

                <div className="telemetry-filter-field">

                    <label
                        htmlFor="satellite-id"
                    >
                        Satellite ID
                    </label>

                    <input
                        id="satellite-id"

                        type="text"

                        value={satelliteId}

                        onChange={(event) =>
                            setSatelliteId(
                                event.target.value
                            )
                        }

                        placeholder="SD-CUBESAT-001"
                    />

                </div>


                <div className="telemetry-filter-field">

                    <label
                        htmlFor="severity"
                    >
                        Severity
                    </label>

                    <select
                        id="severity"

                        value={severity}

                        onChange={(event) =>
                            setSeverity(
                                event.target.value
                            )
                        }
                    >

                        <option value="">
                            All severities
                        </option>

                        <option value="normal">
                            Normal
                        </option>

                        <option value="warning">
                            Warning
                        </option>

                        <option value="critical">
                            Critical
                        </option>

                    </select>

                </div>


                <div className="telemetry-filter-actions">

                    <button
                        type="submit"
                        disabled={loading}
                    >

                        {loading
                            ? "Searching..."
                            : "Apply Filters"
                        }

                    </button>


                    <button
                        type="button"
                        className="telemetry-filter-clear"
                        onClick={handleClear}
                        disabled={loading}
                    >

                        Clear

                    </button>

                </div>

            </form>

        </section>

    );

}