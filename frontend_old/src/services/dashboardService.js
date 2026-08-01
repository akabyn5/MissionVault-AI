const API_BASE_URL = "http://127.0.0.1:8000";

export async function getDashboardData() {
    const response = await fetch(
        `${API_BASE_URL}/telemetry/dashboard`
    );

    if (!response.ok) {
        throw new Error(
            `HTTP Error ${response.status}`
        );
    }

    return await response.json();
}