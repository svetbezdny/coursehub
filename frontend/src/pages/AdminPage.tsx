import { useEffect, useState } from "react";
import { Navigate } from "react-router";

import type { AdminStats } from "../api/admin";
import { getAdminStats } from "../api/admin";
import { ApiError } from "../api/errors";
import { useAuth } from "../auth/useAuth";

function AdminPage() {
	const { user, token, signOut } = useAuth();

	const isAdmin = user?.role === "admin";

	const [stats, setStats] = useState<AdminStats | null>(null);
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		if (!token || !isAdmin) return;

		let ignore = false;

		getAdminStats(token)
			.then((data) => {
				if (!ignore) setStats(data);
			})
			.catch((error: unknown) => {
				if (ignore) return;

				if (error instanceof ApiError && error.status === 401) {
					signOut();
					return;
				}

				setError(
					error instanceof Error
						? error.message
						: "Не удалось загрузить статистику",
				);
			});
		return () => {
			ignore = true;
		};
	}, [token, isAdmin, signOut]);

	if (!user) {
		return <Navigate to="/login" replace state={{ returnTo: "/admin" }} />;
	}

	if (user.role !== "admin") {
		return (
			<main className="page">
				<h1>Недостаточно прав</h1>
			</main>
		);
	}

	return (
		<main className="page">
			<h1>Статистика</h1>
			{!stats && !error && <p role="status">Загружаем статистику…</p>}
			{error && <p role="alert">{error}</p>}
			{stats && (
				<dl className="admin-stats">
					<div>
						<dt>Курсы</dt>
						<dd>{stats.courses}</dd>
					</div>
					<div>
						<dt>Уроки</dt>
						<dd>{stats.lessons}</dd>
					</div>
					<div>
						<dt>Пользователи</dt>
						<dd>{stats.users}</dd>
					</div>
					<div>
						<dt>Записи на курсы</dt>
						<dd>{stats.enrollments}</dd>
					</div>
					<div>
						<dt>Завершения уроков</dt>
						<dd>{stats.completed_lessons}</dd>
					</div>
					<div>
						<dt>Добавления в избранное</dt>
						<dd>{stats.favorite_courses}</dd>
					</div>
				</dl>
			)}
		</main>
	);
}

export default AdminPage;
