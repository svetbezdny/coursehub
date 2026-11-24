import type { Course, CourseCreate } from "../types/course";
import { apiFetch } from "./client";

export async function getCourse(courseId: string): Promise<Course> {
	const response = await apiFetch(`/api/courses/${courseId}`, {
		errorMessage: "Не удалось загрузить курс",
		errorMessages: { 404: "Курс не найден" },
	});

	return response.json();
}

export async function getCourses(
	query: string,
	level: string,
): Promise<Course[]> {
	const params = new URLSearchParams();

	if (query !== "") {
		params.set("q", query);
	}

	if (level !== "") {
		params.set("level", level);
	}

	const response = await apiFetch(`/api/courses?${params.toString()}`, {
		errorMessage: "Не удалось загрузить курсы",
	});

	return response.json();
}

export async function createCourse(
	data: CourseCreate,
	token: string,
): Promise<Course> {
	const response = await apiFetch("/api/courses", {
		method: "POST",
		token,
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(data),
		errorMessage: "Не удалось создать курс",
		errorMessages: {
			401: "Сессия истекла. Войдите снова",
			403: "Недостаточно прав для создания курса",
			422: "Проверьте правильность заполнения полей",
		},
	});

	return response.json();
}
