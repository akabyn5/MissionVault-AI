import { useEffect, useState } from "react";
import Dashboard from "./pages/Dashboard";
import Login from "./pages/Login";

const TOKEN_KEY = "missionvault_access_token";

function App() {
    const [token, setToken] = useState(() => {
        return localStorage.getItem(TOKEN_KEY) || "";
    });

    useEffect(() => {
        if (token) {
            localStorage.setItem(TOKEN_KEY, token);
        } else {
            localStorage.removeItem(TOKEN_KEY);
        }
    }, [token]);

    function handleLogin(newToken) {
        setToken(newToken);
    }

    function handleLogout() {
        setToken("");
    }

    if (!token) {
        return <Login onLogin={handleLogin} />;
    }

    return <Dashboard token={token} onLogout={handleLogout} />;
}

export default App;