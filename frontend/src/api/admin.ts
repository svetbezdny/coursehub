import { apiFetch } from "./client";

export type AdminStats = {
	courses: number;
	lessons: number;
	users: number;
	enrollments: number;
	completed_lessons: number;
	favorite_courses: number;
	reviews: number;
};

export async function getAdminStats(token: string): Promise<AdminStats> {
	const response = await apiFetch("/api/admin/stats", {
		token,
		errorMessage: "Не удалось загрузить статистику",
		errorMessages: { 403: "Статистика доступна только администратору" },
	});

	return response.json();
}
