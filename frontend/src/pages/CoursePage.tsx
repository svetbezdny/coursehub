import { useEffect, useState } from "react";
import { Link, useLocation, useParams } from "react-router";

import { getCourse } from "../api/courses";
import { ApiError } from "../api/errors";
import { enrollInCourse } from "../api/learning";
import { getCourseLessons } from "../api/lessons";
import { useAuth } from "../auth/useAuth";
import LessonList from "../components/LessonList";
import { useCourseProgress } from "../learning/useCourseProgress";
import { useEnrollments } from "../learning/useEnrollments";
import type { Course } from "../types/course";
import type { Lesson } from "../types/lesson";

function CoursePage() {
	const location = useLocation();
	const fromMyCourses = location.state?.from?.split("?")[0] === "/my-courses";

	const { courseId } = useParams();
	const { user, token, signOut } = useAuth();

	const {
		enrollments,
		addEnrollment,
		isLoading: isCheckingEnrollment,
		error: enrollmentsError,
		refresh,
	} = useEnrollments();

	const [course, setCourse] = useState<Course | null>(null);
	const [lessons, setLessons] = useState<Lesson[]>([]);

	const [isEnrolling, setIsEnrolling] = useState(false);
	const [enrollmentError, setEnrollmentError] = useState<string | null>(null);

	const [error, setError] = useState<string | null>(null);
	const [isLoading, setIsLoading] = useState(true);

	const [enrollmentMessage, setEnrollmentMessage] = useState<string>("");

	const isEnrolled = enrollments.some(
		(item) => item.course_id === Number(courseId),
	);

	const {
		completedLessonIds,
		completingLessonId,
		lessonProgressError,
		isProgressLoaded,
		progressLoadError,
		handleCompleteLesson,
	} = useCourseProgress(courseId, isEnrolled);

	const totalLessons = lessons.length;
	const completedLessons = lessons.filter((lesson) =>
		completedLessonIds.includes(lesson.id),
	).length;

	useEffect(() => {
		let ignore = false;

		async function loadCourse() {
			if (courseId === undefined) {
				setError("Не указан идентификатор курса");
				setIsLoading(false);
				return;
			}

			setIsLoading(true);
			setError(null);
			setCourse(null);
			setLessons([]);

			try {
				const [data, lessonsData] = await Promise.all([
					getCourse(courseId),
					getCourseLessons(courseId),
				]);

				if (!ignore) {
					setCourse(data);
					setLessons(lessonsData);
				}
			} catch (error) {
				if (!ignore) {
					setError(error instanceof Error ? error.message : "Ошибка загрузки");
				}
			} finally {
				if (!ignore) {
					setIsLoading(false);
				}
			}
		}
		loadCourse();
		return () => {
			ignore = true;
		};
	}, [courseId]);

	async function handleEnroll() {
		if (!course || isEnrolling || isEnrolled) return;
		if (!token) {
			signOut();
			return;
		}
		setEnrollmentError(null);
		setIsEnrolling(true);

		try {
			const enrollment = await enrollInCourse(course.id, token);
			addEnrollment(enrollment);
			setEnrollmentMessage("Вы успешно записались на курс");
		} catch (error) {
			if (error instanceof ApiError && error.status === 401) {
				signOut();
				return;
			}
			if (
				error instanceof ApiError &&
				error.status === 400 &&
				error.message === "Вы записаны на этот курс"
			) {
				setEnrollmentMessage("Вы записаны на этот курс");
				await refresh();
				return;
			}
			setEnrollmentError(
				error instanceof Error ? error.message : "Ошибка записи на курс",
			);
		} finally {
			setIsEnrolling(false);
		}
	}

	return (
		<main className="page">
			<Link to={location.state?.from ?? "/"}>
				{fromMyCourses ? "К моим курсам" : "К каталогу"}
			</Link>
			{isLoading && <p role="status">Загружаем курс…</p>}
			{error && <p role="alert">{error}</p>}
			{!isLoading && !error && course && (
				<div>
					<h1>{course.title}</h1>
					{(!user ||
						(!isCheckingEnrollment && !isEnrolled && !enrollmentsError)) && (
						<p className="course-price">
							{course.price === 0
								? "Бесплатно"
								: course.price.toLocaleString("ru-RU") + " ₽"}
						</p>
					)}
					<div className="enrollment-actions">
						{!user ? (
							<Link
								to={"/login"}
								state={{
									returnTo: location.pathname + location.search,
									returnState: location.state,
								}}
							>
								Войдите, чтобы записаться
							</Link>
						) : isCheckingEnrollment ? (
							<p role="status">Проверяем запись на курс…</p>
						) : isEnrolled ? (
							!fromMyCourses && (
								<p role="status">
									{enrollmentMessage || "Вы записаны на этот курс"}
								</p>
							)
						) : (
							<button
								type="button"
								className="primary-button"
								disabled={isEnrolling}
								onClick={handleEnroll}
							>
								{isEnrolling ? "Записываем…" : "Записаться на курс"}
							</button>
						)}
						{enrollmentError && <p role="alert">{enrollmentError}</p>}
						{enrollmentsError && <p role="alert">{enrollmentsError}</p>}
					</div>
					<section className="lessons">
						<h2>Программа курса</h2>
						{user && isEnrolled && isProgressLoaded && totalLessons > 0 && (
							<div className="lesson-progress">
								<label htmlFor="course-progress">
									Пройдено {completedLessons} из {totalLessons}
								</label>
								<progress
									id="course-progress"
									value={completedLessons}
									max={totalLessons}
								/>
							</div>
						)}
						{user && isEnrolled && !isProgressLoaded && !progressLoadError && (
							<p role="status">Загружаем прогресс…</p>
						)}
						{progressLoadError && <p role="alert">{progressLoadError}</p>}
						{lessonProgressError && <p role="alert">{lessonProgressError}</p>}
						<LessonList
							lessons={lessons}
							showProgress={Boolean(user && isEnrolled && isProgressLoaded)}
							completedLessonIds={completedLessonIds}
							completingLessonId={completingLessonId}
							onCompleteLesson={handleCompleteLesson}
						/>
					</section>
				</div>
			)}
		</main>
	);
}

export default CoursePage;
