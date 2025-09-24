import React, { useState } from "react";
import myImage from "../res/app_icon.png";
import { API_BASE_URL } from "../config/api";
import { useNavigate } from "react-router-dom";
import { AiOutlineEye, AiOutlineEyeInvisible, AiOutlineArrowLeft } from "react-icons/ai";

function RegisterPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(false);
    const [success, setSuccess] = useState(false);
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);

    const navigate = useNavigate();

    const validatePassword = (pwd) => {
        if (pwd.length < 8) return "The password must be at least 8 characters long";
        if (!/[A-Z]/.test(pwd)) return "The password must contain at least one uppercase letter";
        if (!/[a-z]/.test(pwd)) return "The password must contain at least one lowercase letter";
        if (!/[0-9]/.test(pwd)) return "The password must contain at least one number";
        if (!/[!@#$%^&*(),.?:{}|<>]/.test(pwd)) return "The password must contain at least one special character [!@#$%^&*(),.?:{}|<>]";
        return null;
    };

    const handleRegister = async () => {
        if (password !== confirmPassword) {
            setMessage("❌ the passwords do not match");
            return;
        }

        const pwdError = validatePassword(password);
        if (pwdError) {
            setMessage("❌ " + pwdError);
            return;
        }

        setLoading(true);
        setMessage("");

        try {
            const resp = await fetch(`${API_BASE_URL}/create/user`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ email, password }),
            });

            if (!resp.ok) {
                throw new Error("Registration fail");
            }

            const data = await resp.json();
            setMessage(`✅ Complete signup ${data.email || email}. Now you can login.`);
            setSuccess(true);
        } catch (err) {
            setMessage("❌ Error of signup: " + err.message);
        } finally {
            setLoading(false);
        }
    };

    const handleBackToLogin = () => {
        navigate("/login");
    };

    const renderPasswordInput = (value, setValue, show, setShow, placeholder) => (
        <div style={{ position: "relative", width: "100%" }}>
            <input
                type={show ? "text" : "password"}
                placeholder={placeholder}
                value={value}
                disabled={success}
                onChange={(e) => setValue(e.target.value)}
                style={{
                    width: "100%",
                    padding: "8px 35px 8px 8px",
                    margin: "8px 0",
                    borderRadius: "5px",
                    border: "1px solid #ccc",
                    boxSizing: "border-box"
                }}
                autoComplete="new-password"
            />
            {value && (
                <span
                    onClick={() => setShow(!show)}
                    style={{
                        position: "absolute",
                        right: "8px",
                        top: "50%",
                        transform: "translateY(-50%)",
                        cursor: "pointer",
                        color: "#387EFF",
                        fontSize: "20px",
                        zIndex: 1
                    }}
                >
                    {show ? <AiOutlineEyeInvisible /> : <AiOutlineEye />}
                </span>
            )}
        </div>
    );

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
                maxWidth: "100%",
                textAlign: "center",
                padding: "20px",
                borderRadius: "10px",
                boxShadow: "0 4px 10px rgba(0,0,0,0.1)",
                backgroundColor: "#fff",
                position: "relative"
            }}>
                {/* Pulsante rotondo in alto per tornare al login */}
                <button
                    onClick={handleBackToLogin}
                    style={{
                        position: "absolute",
                        top: "10px",
                        left: "10px",
                        width: "35px",
                        height: "35px",
                        borderRadius: "50%",
                        border: "none",
                        backgroundColor: "#387EFF",
                        color: "white",
                        cursor: "pointer",
                        display: "flex",
                        justifyContent: "center",
                        alignItems: "center"
                    }}
                >
                    <AiOutlineArrowLeft />
                </button>

                <img
                    src={myImage}
                    alt="app_icon"
                    style={{ width: "50%", objectFit: "contain", margin: "0 auto" }}
                />
                <h1 style={{ color: "#387EFF", margin: "20px 0" }}>Register</h1>

                <input
                    type="email"
                    placeholder="Email"
                    value={email}
                    disabled={success}
                    onChange={(e) => setEmail(e.target.value)}
                    style={{
                        width: "100%",
                        padding: "8px",
                        margin: "8px 0",
                        borderRadius: "5px",
                        border: "1px solid #ccc",
                        boxSizing: "border-box"
                    }}
                />

                {renderPasswordInput(password, setPassword, showPassword, setShowPassword, "Password")}
                {renderPasswordInput(confirmPassword, setConfirmPassword, showConfirmPassword, setShowConfirmPassword, "Confirm Password")}

                <button
                    onClick={success ? handleBackToLogin : handleRegister}
                    style={{
                        width: "100%",
                        padding: "10px",
                        marginTop: "10px",
                        borderRadius: "5px",
                        border: "none",
                        backgroundColor: success ? "green" : "#387EFF",
                        color: "white",
                        fontWeight: "bold",
                        cursor: "pointer"
                    }}
                    disabled={loading}
                >
                    {loading ? "Attendere..." : success ? "⬅️ Back to Login" : "Register"}
                </button>

                <div style={{ marginTop: "15px", color: "#333", minHeight: "30px" }}>
                    {loading ? (
                        <div className="spinner" style={{
                            margin: "0 auto",
                            border: "4px solid #f3f3f3",
                            borderTop: "4px solid #387EFF",
                            borderRadius: "50%",
                            width: "24px",
                            height: "24px",
                            animation: "spin 1s linear infinite"
                        }} />
                    ) : (
                        <p>{message}</p>
                    )}
                </div>
            </div>

            <style>{`
                @keyframes spin {
                    0% { transform: rotate(0deg); }
                    100% { transform: rotate(360deg); }
                }
            `}</style>
        </div>
    );
}

export default RegisterPage;
