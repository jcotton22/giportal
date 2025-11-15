// src/App.jsx
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { AuthProvider } from "./AuthContext";
import ProtectedRoute from "./ProtectedRoute";

import RegisterPage from "./pages/RegisterPage";
import ActivatePage from "./pages/ActivatePage";
import Login from "./pages/Login";
import ChangePassword from "./pages/ChangePassword";
import Home from "./pages/Home";
import Unknowns from "./pages/Unknowns";
import ModuleDetails from "./pages/ModuleDetails";
import SlideViewer from "./pages/SlideViewer"

export default function App() {
  return (
    <BrowserRouter>
      <AuthProvider>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/activate" element={<ActivatePage />} />
          <Route
            path="/home"
            element={
              <ProtectedRoute>
                <Home />
              </ProtectedRoute>
            }
          />
          <Route 
            path = '/unknowns'
            element={
              <ProtectedRoute>
                <Unknowns />
              </ProtectedRoute>
            }
          />
          <Route
            path="/change-password"
            element={
              <ProtectedRoute>
                <ChangePassword />
              </ProtectedRoute>
            }
          />
          <Route
            path = "/modules/:moduleId/"
            element = {
              <ProtectedRoute>
                <ModuleDetails/>
              </ProtectedRoute>
            }
          />
          <Route 
            path = "/slides/:slideId"
            element = {
              <ProtectedRoute>
                <SlideViewer/>
              </ProtectedRoute>
            }
          />
          <Route path="*" element={<Login />} />
        </Routes>
      </AuthProvider>
    </BrowserRouter>
  );
}
