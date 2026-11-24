import type { Lesson } from "../types/lesson";
import { apiFetch } from "./client";

export async function getCourseLessons(courseId: string): Promise<Lesson[]> {
	const response = await apiFetch(`/api/courses/${courseId}/lessons`, {
		errorMessage: "Не удалось загрузить уроки",
	});

	return response.json();
}
