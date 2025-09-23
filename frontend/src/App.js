import React from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import LoginPage from "./pages/login-page";
import HomePage from "./pages/home-page";
import RegisterProfilePage from "./pages/register-profilePage";

function App() {
    return (
        <Router>
            <Routes>
                {/* Rotta principale → login */}
                <Route path="/" element={<LoginPage />} />

                {/* Rotta esplicita per login */}
                <Route path="/login" element={<LoginPage />} />

                {/* Rotta per la home */}
                <Route path="/home" element={<HomePage />} />

                {/* Rotta per la registrazione */}
                <Route path="/register" element={<RegisterProfilePage />} />

                {/* Rotta fallback → se l’utente mette un URL non valido */}
                <Route path="*" element={<h1>404 - Pagina non trovata</h1>} />
            </Routes>
        </Router>
    );
}

export default App;
