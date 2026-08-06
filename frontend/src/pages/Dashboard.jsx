import { useEffect, useState } from "react";

import { getDashboardData } from "../services/dashboardService";

import MissionStatusCard from "../components/MissionStatusCard";
import LatestTelemetryCard from "../components/LatestTelemetryCard";
import StatisticsCard from "../components/StatisticsCard";
import MetricsCard from "../components/MetricsCard";
import TrendsCard from "../components/TrendsCard";
import AlertsCard from "../components/AlertsCard";

const REFRESH_INTERVAL = 5000;

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

            console.error("Failed to load dashboard:", err);

            setError(err.message);

        } finally {

            setLoading(false);

        }

    }

    useEffect(() => {

        // Load data immediately when the dashboard starts.
        loadDashboard();

        // Refresh dashboard data every 5 seconds.
        const intervalId = setInterval(() => {

            loadDashboard();

        }, REFRESH_INTERVAL);

        // Stop refreshing when the component is unmounted.
        return () => {

            clearInterval(intervalId);

        };

    }, []);

    if (loading) {

        return (
            <div>
                <h2>Loading Mission Dashboard...</h2>
            </div>
        );

    }

    if (error) {

        return (
            <div>
                <h2>MissionVault AI</h2>
                <p>Failed to load dashboard.</p>
                <p>{error}</p>
            </div>
        );

    }

    if (!dashboard) {

        return (
            <div>
                <h2>No dashboard data available.</h2>
            </div>
        );

    }

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