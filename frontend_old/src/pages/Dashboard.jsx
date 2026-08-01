import { useEffect, useState } from "react";

import { getDashboardData } from "../services/dashboardService";

export default function Dashboard() {

    const [dashboard, setDashboard] = useState(null);

    const [loading, setLoading] = useState(true);

    const [error, setError] = useState(null);

    async function loadDashboard() {

        try {

            const data = await getDashboardData();

            setDashboard(data);

            setError(null);

        } catch (err) {

            setError(err.message);

        } finally {

            setLoading(false);

        }

    }

    useEffect(() => {

        loadDashboard();

        const interval = setInterval(() => {

            loadDashboard();

        }, 5000);

        return () => clearInterval(interval);

    }, []);

    if (loading) {

        return <h2>Loading Mission Dashboard...</h2>;

    }

    if (error) {

        return <h2>Error: {error}</h2>;

    }

    return (

        <div>

            <h1>MissionVault AI</h1>

            <pre>

                {JSON.stringify(dashboard, null, 2)}

            </pre>

        </div>

    );

}