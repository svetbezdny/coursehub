import { useEffect, useState } from "react";
import { Link, useSearchParams } from "react-router";

import { getCourses } from "../api/courses";
import { useAuth } from "../auth/useAuth";
import CourseCard from "../components/CourseCard";
import { useFavorites } from "../learning/useFavorites";
import type { Course } from "../types/course";

function CoursesPage() {
	const [searchParams, setSearchParams] = useSearchParams();

	const [courses, setCourses] = useState<Course[]>([]);
	const [error, setError] = useState<string | null>(null);
	const [isLoading, setIsLoading] = useState(true);

	const query = searchParams.get("q") ?? "";
	const level = searchParams.get("level") ?? "";

	const { user, token } = useAuth();

	const [debouncedQuery, setDebouncedQuery] = useState(query);

	function updateFilter(name: string, value: string) {
		const params = new URLSearchParams(searchParams);
		if (value !== "") {
			params.set(name, value);
		} else {
			params.delete(name);
		}

		setSearchParams(params, { replace: true });
	}

	useEffect(() => {
		const timer = setTimeout(() => setDebouncedQuery(query), 300);
		return () => clearTimeout(timer);
	}, [query]);

	useEffect(() => {
		let ignore = false;

		async function loadCourses() {
			const searchQuery = debouncedQuery.trim();

			if (searchQuery.length > 0 && searchQuery.length < 2) {
				setError("Введите минимум 2 символа для поиска");
				setIsLoading(false);
				return;
			}
			setIsLoading(true);
			setError(null);

			try {
				const data: Course[] = await getCourses(searchQuery, level);
				if (!ignore) {
					setCourses(data);
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
		loadCourses();
		return () => {
			ignore = true;
		};
	}, [debouncedQuery, level]);

	const { favoriteIds, favoritesError, pendingFavoriteIds, toggleFavorite } =
		useFavorites();

	return (
		<main className="page">
			<header className="page-header">
				<h1>Каталог курсов</h1>
				{(user?.role === "admin" || user?.role === "author") && (
					<Link to={"/courses/new"}>Создать курс</Link>
				)}
			</header>
			<div className="filters">
				<label className="search-field">
					Поиск
					<input
						type="search"
						placeholder="Название курса"
						value={query}
						onChange={(e) => updateFilter("q", e.target.value)}
					/>
				</label>
				<label className="search-field">
					Уровень
					<select
						value={level}
						onChange={(e) => updateFilter("level", e.target.value)}
					>
						<option value="">Все уровни</option>
						<option value="beginner">Начальный</option>
						<option value="intermediate">Средний</option>
						<option value="advanced">Продвинутый</option>
					</select>
				</label>
				<button
					type="button"
					className="reset-filters"
					onClick={() => setSearchParams({}, { replace: true })}
					disabled={query === "" && level === ""}
				>
					Сбросить фильтры
				</button>
			</div>
			{isLoading && <p role="status">Загружаем курсы…</p>}
			{error && <p role="alert">{error}</p>}
			{!isLoading && !error && courses.length === 0 && (
				<p>
					{query.trim() !== "" || level !== ""
						? "По выбранным условиям курсы не найдены"
						: "Курсов пока нет"}
				</p>
			)}
			{!isLoading && !error && courses.length > 0 && (
				<p className="results-count">
					{query.trim() !== "" || level !== ""
						? "Найдено курсов"
						: "Всего курсов"}
					: {courses.length}
				</p>
			)}
			{favoritesError && <p role="alert">{favoritesError}</p>}
			{!isLoading && !error && (
				<section className="courses">
					{courses.map((course) => (
						<CourseCard
							key={course.id}
							course={course}
							isFavorite={favoriteIds?.includes(course.id) ?? false}
							isFavoritePending={pendingFavoriteIds.includes(course.id)}
							onToggleFavorite={
								token && favoriteIds !== null
									? () => toggleFavorite(course.id)
									: undefined
							}
						/>
					))}
				</section>
			)}
		</main>
	);
}

export default CoursesPage;
