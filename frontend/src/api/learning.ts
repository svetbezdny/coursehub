import type { FavoriteCourse } from "../types/course";
import type { Enrollment } from "../types/enrollment";
import type { CourseProgress, LessonProgress } from "../types/lesson";
import { apiFetch } from "./client";

const sessionExpiredMessage = "Сессия истекла. Войдите снова";

export async function enrollInCourse(
	courseId: number,
	token: string,
): Promise<Enrollment> {
	const response = await apiFetch(`/api/courses/${courseId}/enroll`, {
		method: "POST",
		token,
		errorMessage: "Не удалось записаться на курс",
		errorMessages: {
			401: sessionExpiredMessage,
			403: "Недостаточно прав для записи на курс",
			404: "Курс не найден",
		},
		errorDetails: {
			"User is already enrolled in this course": "Вы записаны на этот курс",
		},
	});

	return response.json();
}

export async function getMyEnrollments(token: string): Promise<Enrollment[]> {
	const response = await apiFetch("/api/me/enrollments", {
		token,
		errorMessage: "Не удалось загрузить ваши курсы",
		errorMessages: { 401: sessionExpiredMessage },
	});

	return response.json();
}

export async function completeLesson(
	lessonId: number,
	token: string,
): Promise<LessonProgress> {
	const response = await apiFetch(`/api/lessons/${lessonId}/complete`, {
		method: "POST",
		token,
		errorMessage: "Не удалось отметить урок завершённым",
		errorMessages: {
			401: sessionExpiredMessage,
			403: "Недостаточно прав для завершения урока",
			404: "Урок не найден",
		},
		errorDetails: {
			"Enroll in course before completing lessons":
				"Сначала запишитесь на курс",
		},
	});

	return response.json();
}

export async function getMyProgress(token: string): Promise<CourseProgress[]> {
	const response = await apiFetch("/api/me/progress", {
		token,
		errorMessage: "Не удалось загрузить прогресс",
		errorMessages: { 401: sessionExpiredMessage },
	});

	return response.json();
}

export async function getMyFavorites(token: string): Promise<FavoriteCourse[]> {
	const response = await apiFetch("/api/me/favorites", {
		token,
		errorMessage: "Не удалось загрузить избранные курсы",
		errorMessages: { 401: sessionExpiredMessage },
	});

	return response.json();
}

export async function addFavoriteCourse(
	courseId: number,
	token: string,
): Promise<FavoriteCourse> {
	const response = await apiFetch(`/api/courses/${courseId}/favorite`, {
		method: "POST",
		token,
		errorMessage: "Не удалось добавить курс в избранное",
		errorMessages: { 401: sessionExpiredMessage },
	});

	return response.json();
}

export async function removeFavoriteCourse(
	courseId: number,
	token: string,
): Promise<void> {
	await apiFetch(`/api/courses/${courseId}/favorite`, {
		method: "DELETE",
		token,
		errorMessage: "Не удалось удалить курс из избранного",
		errorMessages: { 401: sessionExpiredMessage },
	});
}
