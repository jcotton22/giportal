// src/ProtectedRoute.jsx
import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";
import AuthenticatedLayout from "./pages/AuthenticatedLayout";

export default function ProtectedRoute({ children }) {
  const { ready, isAuthenticated } = useAuth();

  if (!ready) return null;

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  // Wrap authenticated content inside the layout (adds navbar)
  return <AuthenticatedLayout>{children}</AuthenticatedLayout>;
}
