import React, { useState } from "react";
import myImage from "../res/app_icon.png";
import { API_BASE_URL } from "../config/api";
import { useNavigate } from "react-router-dom";
import { useDispatch } from 'react-redux';
import { setUserId } from '../store/userSlice';

function LoginPage() {
    const [identifier, setIdentifier] = useState("");
    const [password, setPassword] = useState("");
    const [message, setMessage] = useState("");
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const handleLogin = async () => {
        try {
            const resp = await fetch(`${API_BASE_URL}/login/user`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ identifier, password }),
            });

            if (!resp.ok) {
                throw new Error("Login fallito");
            }

            const data = await resp.json();
            setMessage(`✅ Benvenuto ${data.user_id || "utente"}`);

            // ✅ salva solo lo userId nello store
            dispatch(setUserId(data.user_id));

            // ✅ reindirizza alla home
            navigate("/home");
        } catch (err) {
            setMessage("❌ Errore di login: " + err.message);
        }
    };

    const handleGoToRegister = () => {
        navigate("/register");
    };

    return (
        <div style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: "100vh",
            backgroundColor: "#f9f9f9"
        }}>
            <div style={{
                width: "300px",
                textAlign: "center",
                padding: "20px",
                borderRadius: "10px",
                boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
                backgroundColor: "#fff"
            }}>
                <img
                    src={myImage}
                    alt="app_icon"
                    style={{ width: "50%", objectFit: "contain", margin: "0 auto" }}
                />
                <h1 style={{ color: "#387EFF", margin: "20px 0" }}>Login</h1>
                <input
                    type="text"
                    placeholder="Identifier"
                    value={identifier}
                    onChange={(e) => setIdentifier(e.target.value)}
                    style={{ width: "100%", padding: "8px", margin: "8px 0", borderRadius: "5px", border: "1px solid #ccc" }}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    style={{ width: "100%", padding: "8px", margin: "8px 0", borderRadius: "5px", border: "1px solid #ccc" }}
                />
                <button
                    onClick={handleLogin}
                    style={{
                        width: "100%",
                        padding: "10px",
                        marginTop: "10px",
                        borderRadius: "5px",
                        border: "none",
                        backgroundColor: "#387EFF",
                        color: "white",
                        fontWeight: "bold",
                        cursor: "pointer"
                    }}
                >
                    Login
                </button>

                <button
                    onClick={handleGoToRegister}
                    style={{
                        width: "100%",
                        padding: "10px",
                        marginTop: "10px",
                        borderRadius: "5px",
                        border: "1px solid #387EFF",
                        backgroundColor: "#fff",
                        color: "#387EFF",
                        fontWeight: "bold",
                        cursor: "pointer"
                    }}
                >
                    Non hai un account? Registrati
                </button>

                <p style={{ marginTop: "15px", color: "#333" }}>{message}</p>
            </div>
        </div>
    );
}

export default LoginPage;
