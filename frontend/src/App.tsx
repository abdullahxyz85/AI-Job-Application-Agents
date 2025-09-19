import React from "react";
import {
  BrowserRouter as Router,
  Routes,
  Route,
  Navigate,
} from "react-router-dom";
import { motion } from "framer-motion";
import { ThemeProvider } from "./contexts/ThemeContext";
import { AuthProvider, useAuth } from "./contexts/AuthContext";
import { ToastProvider } from "./components/Toast";
import Navigation from "./components/Navigation";
import ProtectedRoute from "./components/ProtectedRoute";
import LoadingSpinner from "./components/LoadingSpinner";
import SignInPage from "./pages/SignInPage";
import SignUpPage from "./pages/SignUpPage";
import LandingPage from "./pages/LandingPage";
import Dashboard from "./pages/Dashboard";
import AIJobApplication from "./pages/AIJobApplication";
import AuditLog from "./pages/AuditLog";
import Profile from "./pages/Profile";
import Settings from "./pages/Settings";

const AppRoutes: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return <LoadingSpinner message="Initializing..." />;
  }

  return (
    <Routes>
      {/* Public routes */}
      <Route path="/" element={<LandingPage />} />
      <Route
        path="/signin"
        element={
          isAuthenticated ? (
            <Navigate to="/dashboard" replace />
          ) : (
            <SignInPage />
          )
        }
      />
      <Route
        path="/signup"
        element={
          isAuthenticated ? (
            <Navigate to="/dashboard" replace />
          ) : (
            <SignUpPage />
          )
        }
      />

      {/* Protected routes with Navigation */}
      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <>
              <Navigation />
              <Routes>
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/ai-application" element={<AIJobApplication />} />
                <Route path="/audit" element={<AuditLog />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/settings" element={<Settings />} />
                <Route
                  path="*"
                  element={<Navigate to="/dashboard" replace />}
                />
              </Routes>
            </>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
};

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.3 }}
            className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200"
          >
            <AppRoutes />
            <ToastProvider />
          </motion.div>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
