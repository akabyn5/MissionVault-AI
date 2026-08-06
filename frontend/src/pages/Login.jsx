import { useState } from "react";
import { login } from "../services/authService";

export default function Login({ onLogin }) {
    const [username, setUsername] = useState("operator");
    const [password, setPassword] = useState("SpaceDogs2026");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    async function handleSubmit(event) {
        event.preventDefault();
        setLoading(true);
        setError(null);

        try {
            const data = await login({
                username,
                password
            });

            onLogin(data.access_token);
        } catch (err) {
            setError(err.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="auth-shell">
            <section className="auth-card">
                <h1>MissionVault AI</h1>
                <h2>Operator Login</h2>
                <p className="auth-hint">
                    Use the demo operator account to access the dashboard.
                </p>

                <form className="auth-form" onSubmit={handleSubmit}>
                    <label>
                        Username
                        <input
                            type="text"
                            value={username}
                            onChange={(e) => setUsername(e.target.value)}
                            autoComplete="username"
                        />
                    </label>

                    <label>
                        Password
                        <input
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            autoComplete="current-password"
                        />
                    </label>

                    {error && <p className="auth-error">{error}</p>}

                    <button type="submit" disabled={loading}>
                        {loading ? "Signing in..." : "Sign in"}
                    </button>
                </form>
            </section>
        </div>
    );
}