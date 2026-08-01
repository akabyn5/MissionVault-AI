import { useEffect, useState } from "react";

import { getDashboardData } from "../services/dashboardService";

import MissionStatusCard from "../components/MissionStatusCard";
import LatestTelemetryCard from "../components/LatestTelemetryCard";
import StatisticsCard from "../components/StatisticsCard";
import MetricsCard from "../components/MetricsCard";
import TrendsCard from "../components/TrendsCard";
import AlertsCard from "../components/AlertsCard";

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

        const interval = setInterval(loadDashboard, 5000);

        return () => clearInterval(interval);

    }, []);

    if (loading) return <h2>Loading...</h2>;

    if (error) return <h2>{error}</h2>;

    return (

        <div>

            <h1>MissionVault AI</h1>

            <MissionStatusCard
                status={dashboard.mission_status}
            />

            <LatestTelemetryCard
                latest={dashboard.latest}
            />

            <StatisticsCard
                statistics={dashboard.statistics}
            />

            <MetricsCard
                metrics={dashboard.metrics}
            />

            <TrendsCard
                trends={dashboard.trends}
            />

            <AlertsCard
                alerts={dashboard.alerts}
            />

        </div>

    );

}