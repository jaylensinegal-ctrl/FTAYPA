import { Navigate, Route, Routes } from "react-router-dom";
import Navbar from "./components/Navbar";
import ProtectedRoute from "./components/ProtectedRoute";
import { AuthProvider } from "./context/AuthContext";
import { useAuth } from "./context/AuthContext";
import LandingSequencePage from "./pages/LandingSequencePage";
import HomePage from "./pages/HomePage";
import ProgramsPage from "./pages/ProgramsPage";
import FlightSystemPage from "./pages/FlightSystemPage";
import DashboardPage from "./pages/DashboardPage";
import LeaderboardPage from "./pages/LeaderboardPage";
import AboutPage from "./pages/AboutPage";
import CoachLabPage from "./pages/CoachLabPage";
import MembershipPage from "./pages/MembershipPage";
import MembershipSuccessPage from "./pages/MembershipSuccessPage";
import MembershipCancelPage from "./pages/MembershipCancelPage";
import EventsPage from "./pages/EventsPage";
import ClearancePage from "./pages/ClearancePage";
import LoginPage from "./pages/LoginPage";
import AcceptInvitePage from "./pages/AcceptInvitePage";
import AccessCenterPage from "./pages/AccessCenterPage";

function App() {
  return (
    <AuthProvider>
      <div className="app-shell">
        <Navbar />
        <main className="page-container">
          <Routes>
            <Route path="/" element={<RoleAwareStartPage />} />
            <Route path="/flight-deck" element={<HomePage />} />
            <Route
              path="/mission"
              element={(
                <ProtectedRoute allowGuests blockedRoles={["athlete"]}>
                  <ProgramsPage />
                </ProtectedRoute>
              )}
            />
            <Route
              path="/hangar"
              element={(
                <ProtectedRoute allowedRoles={["coach", "admin"]}>
                  <CoachLabPage />
                </ProtectedRoute>
              )}
            />
            <Route path="/wings" element={<LeaderboardPage />} />
            <Route path="/programs" element={<Navigate to="/mission" replace />} />
            <Route path="/flight-system" element={<FlightSystemPage />} />
            <Route
              path="/dashboard"
              element={(
                <ProtectedRoute allowedRoles={["coach", "parent", "athlete", "admin"]}>
                  <DashboardPage />
                </ProtectedRoute>
              )}
            />
            <Route path="/leaderboard" element={<Navigate to="/wings" replace />} />
            <Route path="/coach-lab" element={<Navigate to="/hangar" replace />} />
            <Route
              path="/membership"
              element={(
                <ProtectedRoute allowGuests blockedRoles={["athlete"]}>
                  <MembershipPage />
                </ProtectedRoute>
              )}
            />
            <Route
              path="/membership/success"
              element={(
                <ProtectedRoute allowGuests blockedRoles={["athlete"]}>
                  <MembershipSuccessPage />
                </ProtectedRoute>
              )}
            />
            <Route
              path="/membership/cancel"
              element={(
                <ProtectedRoute allowGuests blockedRoles={["athlete"]}>
                  <MembershipCancelPage />
                </ProtectedRoute>
              )}
            />
            <Route path="/events" element={<EventsPage />} />
            <Route
              path="/clearance"
              element={(
                <ProtectedRoute allowGuests blockedRoles={["athlete"]}>
                  <ClearancePage />
                </ProtectedRoute>
              )}
            />
            <Route path="/about" element={<AboutPage />} />
            <Route path="/login" element={<LoginPage />} />
            <Route path="/accept-invite" element={<AcceptInvitePage />} />
            <Route
              path="/access-center"
              element={(
                <ProtectedRoute allowedRoles={["coach", "admin"]}>
                  <AccessCenterPage />
                </ProtectedRoute>
              )}
            />
            <Route path="*" element={<Navigate to="/flight-deck" replace />} />
          </Routes>
        </main>
      </div>
    </AuthProvider>
  );
}

function RoleAwareStartPage() {
  const { isAuthenticated, loading, user } = useAuth();

  if (loading) {
    return (
      <section className="panel auth-shell">
        <p className="eyebrow">FlightTime Access</p>
        <h1>Loading your route…</h1>
      </section>
    );
  }

  if (isAuthenticated && (user?.role === "athlete" || user?.role === "parent")) {
    return <Navigate to="/dashboard" replace />;
  }

  return <LandingSequencePage />;
}

export default App;
