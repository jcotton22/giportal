// src/App.jsx
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import ProtectedRoute from "./pages/ProtectedRoute";

import NotFound from "./pages/NotFound";
import Login from "./pages/Login";
import Home from "./pages/Home";
import Unknowns from "./pages/Unknowns";
import ModuleDetails from "./pages/ModuleDetails";
import SlideViewer from "./pages/SlideViewer"
import Register from "./pages/Register";

function Logout () {
  localStorage.clear();
  return <Navigate to ='/login' />
}

function RegisterAndLogout() {
  localStorage.clear();
  return <Register />
}

export default function App() {
  return (
    <BrowserRouter>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/register" element={<RegisterAndLogout />} />
          <Route path = "/logout" element = {<Logout />} />
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
          <Route path="*" element={<NotFound />} />
        </Routes>
    </BrowserRouter>
  );
}
