const API_BASE_URL = "http://127.0.0.1:8000";

export async function login({ username, password }) {
    const response = await fetch(
        `${API_BASE_URL}/auth/login`,
        {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                username,
                password
            })
        }
    );

    if (!response.ok) {
        throw new Error("Invalid username or password");
    }

    return await response.json();
}

export async function getCurrentUser(token) {
    const response = await fetch(
        `${API_BASE_URL}/auth/me`,
        {
            headers: {
                Authorization: `Bearer ${token}`
            }
        }
    );

    if (!response.ok) {
        throw new Error("UNAUTHORIZED");
    }

    return await response.json();
}