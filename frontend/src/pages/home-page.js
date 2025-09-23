import React, { useState, useEffect } from "react";
import axios from "axios";
import myImage from "../res/app_icon.png";
import { API_BASE_URL } from "../config/api";
import { useSelector } from "react-redux";

function UserHomePage() {
    // ✅ leggi userId dallo store Redux
    const userId = useSelector((state) => state.user.userId);

    const [empathy, setEmpathy] = useState(4);
    const [humor, setHumor] = useState(4);
    const [optimism, setOptimism] = useState(4);

    const [isEditing, setIsEditing] = useState(false);

    // fetch dei valori iniziali dal backend
    const fetchUserData = async () => {
        if (!userId) return; // protezione se userId non presente
        try {
            const res = await axios.get(`${API_BASE_URL}/user`, {
                params: { identifier: userId }
            });

            if (res.data?.params) {
                setEmpathy(res.data.params.empathy ?? 4);
                setHumor(res.data.params.humor ?? 4);
                setOptimism(res.data.params.optimism ?? 4);
            }
        } catch (err) {
            console.error("Error fetching user data:", err);
        }
    };

    useEffect(() => {
        fetchUserData();
    }, [userId]);

    const toggleEdit = async () => {
        if (!userId) return;
        if (isEditing) {
            try {
                // POST dei nuovi valori
                await axios.put(`${API_BASE_URL}/user`, {
                    user_id: userId,
                    params: {
                        empathy,
                        humor,
                        optimism
                    }
                });

                // REFRESH dei dati dal backend per coerenza
                await fetchUserData();
                console.log("Values saved and refreshed successfully!");
            } catch (err) {
                console.error("Error saving or refreshing user data:", err);
            }
        }
        setIsEditing(prev => !prev);
    };

    const sliderStyle = {
        width: "100%",
        margin: "10px 0"
    };

    const labelStyle = {
        textAlign: "left",
        marginTop: "10px",
        fontWeight: "bold",
        color: "#333"
    };

    if (!userId) return <p>Loading user info...</p>; // fallback se userId non è ancora disponibile

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
                <h1 style={{ color: "#387EFF", margin: "20px 0 10px 0" }}>Profile</h1>
                <h3 style={{ color: "#387EFF", margin: "0 0 20px 0" }}>User : {userId}</h3>

                <div style={labelStyle}>Empathy: {empathy}</div>
                <input
                    type="range"
                    min="1"
                    max="5"
                    value={empathy}
                    onChange={(e) => setEmpathy(Number(e.target.value))}
                    style={sliderStyle}
                    disabled={!isEditing}
                />

                <div style={labelStyle}>Humor: {humor}</div>
                <input
                    type="range"
                    min="1"
                    max="5"
                    value={humor}
                    onChange={(e) => setHumor(Number(e.target.value))}
                    style={sliderStyle}
                    disabled={!isEditing}
                />

                <div style={labelStyle}>Optimism: {optimism}</div>
                <input
                    type="range"
                    min="1"
                    max="5"
                    value={optimism}
                    onChange={(e) => setOptimism(Number(e.target.value))}
                    style={sliderStyle}
                    disabled={!isEditing}
                />

                <button
                    onClick={toggleEdit}
                    style={{
                        width: "100%",
                        padding: "10px",
                        marginTop: "20px",
                        borderRadius: "5px",
                        border: "none",
                        backgroundColor: isEditing ? "#FF5733" : "#387EFF",
                        color: "white",
                        fontWeight: "bold",
                        cursor: "pointer"
                    }}
                >
                    {isEditing ? "Save & Back to Profile" : "Edit Profile"}
                </button>
            </div>
        </div>
    );
}

export default UserHomePage;
