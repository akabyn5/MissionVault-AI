const API_BASE_URL = "http://127.0.0.1:8000";

async function apiFetch(path, token) {
    const headers = {};

    if (token) {
        headers.Authorization = `Bearer ${token}`;
    }

    const response = await fetch(`${API_BASE_URL}${path}`, {
        headers
    });

    if (response.status === 401) {
        throw new Error("UNAUTHORIZED");
    }

    if (!response.ok) {
        throw new Error(`HTTP Error ${response.status}`);
    }

    return await response.json();
}

export async function getDashboardData(token) {
    return await apiFetch("/telemetry/dashboard", token);
}

export async function searchTelemetry({
    satelliteId = "",
    severity = "",
    limit = 100,
    token = ""
} = {}) {
    const params = new URLSearchParams();

    if (satelliteId) {
        params.set("satellite_id", satelliteId);
    }

    if (severity) {
        params.set("severity", severity);
    }

    params.set("limit", String(limit));

    return await apiFetch(`/telemetry/search?${params.toString()}`, token);
}