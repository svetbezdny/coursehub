import { useEffect, useState } from "react";

import { ApiError } from "../api/errors";
import { completeLesson, getMyProgress } from "../api/learning";
import { useAuth } from "../auth/useAuth";

export function useCourseProgress(
	courseId: string | undefined,
	isEnrolled: boolean,
) {
	const { token, signOut } = useAuth();

	const [completedLessonIds, setCompletedLessonIds] = useState<number[]>([]);
	const [completingLessonId, setCompletingLessonId] = useState<number | null>(
		null,
	);
	const [lessonProgressError, setLessonProgressError] = useState<string | null>(
		null,
	);
	const [isProgressLoaded, setIsProgressLoaded] = useState(false);
	const [progressLoadError, setProgressLoadError] = useState<string | null>(
		null,
	);

	useEffect(() => {
		if (!token || !courseId || !isEnrolled) return;

		let ignore = false;
		getMyProgress(token)
			.then((rows) => {
				if (ignore) return;

				const progress = rows.find(
					(item) => item.course_id === Number(courseId),
				);
				if (!progress) {
					setProgressLoadError("Прогресс этого курса не найден");
					return;
				}

				setCompletedLessonIds(progress.completed_lesson_ids);
				setProgressLoadError(null);
				setIsProgressLoaded(true);
			})
			.catch((error: unknown) => {
				if (ignore) return;

				if (error instanceof ApiError && error.status === 401) {
					signOut();
					return;
				}

				setProgressLoadError(
					error instanceof Error
						? error.message
						: "Не удалось загрузить прогресс",
				);
			});

		return () => {
			ignore = true;
		};
	}, [token, courseId, isEnrolled, signOut]);

	async function handleCompleteLesson(lessonId: number) {
		if (
			!courseId ||
			!isEnrolled ||
			completingLessonId !== null ||
			completedLessonIds.includes(lessonId)
		)
			return;

		if (!token) {
			signOut();
			return;
		}

		setLessonProgressError(null);
		setCompletingLessonId(lessonId);

		try {
			const progress = await completeLesson(lessonId, token);
			if (progress.completed) {
				setCompletedLessonIds((current) =>
					current.includes(progress.lesson_id)
						? current
						: [...current, progress.lesson_id],
				);
			}
		} catch (error) {
			if (error instanceof ApiError && error.status === 401) signOut();
			else
				setLessonProgressError(
					error instanceof Error ? error.message : "Ошибка завершения урока",
				);
		} finally {
			setCompletingLessonId(null);
		}
	}

	return {
		completedLessonIds,
		completingLessonId,
		lessonProgressError,
		isProgressLoaded,
		progressLoadError,
		handleCompleteLesson,
	};
}
