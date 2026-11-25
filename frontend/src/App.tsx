import "./App.css";

import { Route, Routes, useLocation } from "react-router";

import { useAuth } from "./auth/useAuth";
import SiteHeader from "./components/SiteHeader";
import EnrollmentsProvider from "./learning/EnrollmentsProvider";
import AdminPage from "./pages/AdminPage";
import CoursePage from "./pages/CoursePage";
import CoursesPage from "./pages/CoursesPage";
import CreateCoursePage from "./pages/CreateCoursePage";
import LoginPage from "./pages/LoginPage";
import MyCoursesPage from "./pages/MyCoursesPage";
import NotFoundPage from "./pages/NotFoundPage";
import RegisterPage from "./pages/RegisterPage";

function App() {
	const { user, isInitializing } = useAuth();
	const location = useLocation();

	if (isInitializing) {
		return (
			<main className="page">
				<p role="status">Проверяем сессию…</p>
			</main>
		);
	}
	return (
		<EnrollmentsProvider key={user?.id ?? "guest"}>
			<SiteHeader />
			<Routes>
				<Route path="/" element={<CoursesPage />} />
				<Route
					path="/courses/:courseId"
					element={
						<CoursePage key={location.pathname + ":" + (user?.id ?? "guest")} />
					}
				/>
				<Route path="/courses/new" element={<CreateCoursePage />} />
				<Route path="/login" element={<LoginPage />} />
				<Route path="/register" element={<RegisterPage />} />
				<Route path="/my-courses" element={<MyCoursesPage />} />
				{user?.role === "admin" && (
					<Route path="/admin" element={<AdminPage />} />
				)}
				<Route path="*" element={<NotFoundPage />} />
			</Routes>
		</EnrollmentsProvider>
	);
}

export default App;
