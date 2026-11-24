import { Link, Navigate, useLocation, useSearchParams } from "react-router";

import { useAuth } from "../auth/useAuth";
import FavoriteButton from "../components/FavoriteButton";
import { useEnrollments } from "../learning/useEnrollments";
import { useFavorites } from "../learning/useFavorites";

function MyCoursesPage() {
	const { user } = useAuth();
	const { enrollments, isLoading, error } = useEnrollments();

	const {
		favorites,
		favoriteIds,
		favoritesError,
		pendingFavoriteIds,
		toggleFavorite,
	} = useFavorites();

	const [searchParams] = useSearchParams();
	const showFavorites = searchParams.get("tab") === "favorites";

	const location = useLocation();

	if (!user) {
		return (
			<Navigate
				to={"/login"}
				replace
				state={{ returnTo: location.pathname + location.search }}
			/>
		);
	}

	return (
		<main className="page">
			<Link to={"/"} className="back-link">
				К каталогу
			</Link>
			<h1>Мои курсы</h1>
			<nav className="my-courses-tabs" aria-label="Разделы моих курсов">
				<Link
					to="/my-courses"
					aria-current={!showFavorites ? "page" : undefined}
				>
					Я учусь
				</Link>
				<Link
					to="/my-courses?tab=favorites"
					aria-current={showFavorites ? "page" : undefined}
				>
					Избранное
				</Link>
			</nav>
			{favoritesError && <p role="alert">{favoritesError}</p>}
			{!showFavorites && (
				<section aria-label="Я учусь">
					{isLoading && <p role="status">Загружаем ваши курсы…</p>}
					{error && <p role="alert">{error}</p>}
					{!isLoading && !error && enrollments.length === 0 && (
						<p>Вы пока не записаны ни на один курс</p>
					)}
					{!isLoading && !error && enrollments.length > 0 && (
						<section className="courses">
							{enrollments.map((enrollment) => (
								<article className="course-card" key={enrollment.id}>
									<div className="course-card-top">
										<h2>
											<Link
												to={`/courses/${enrollment.course_id}`}
												state={{ from: "/my-courses" }}
											>
												{enrollment.course_title}
											</Link>
										</h2>
										{favoriteIds !== null && (
											<FavoriteButton
												title={enrollment.course_title}
												isFavorite={favoriteIds.includes(enrollment.course_id)}
												isFavoritePending={pendingFavoriteIds.includes(
													enrollment.course_id,
												)}
												onToggleFavorite={() =>
													toggleFavorite(enrollment.course_id)
												}
											/>
										)}
									</div>
								</article>
							))}
						</section>
					)}
				</section>
			)}
			{showFavorites && (
				<section aria-label="Избранное">
					{favorites === null && !favoritesError && (
						<p role="status">Загружаем избранное…</p>
					)}
					{favorites?.length === 0 && <p>Пока нет избранных курсов</p>}
					{favorites && favorites.length > 0 && (
						<div className="courses">
							{favorites.map((favorite) => (
								<article className="course-card" key={favorite.id}>
									<div className="course-card-top">
										<h2>
											<Link
												to={`/courses/${favorite.course_id}`}
												state={{ from: "/my-courses?tab=favorites" }}
											>
												{favorite.course_title}
											</Link>
										</h2>
										<FavoriteButton
											title={favorite.course_title}
											isFavorite
											isFavoritePending={pendingFavoriteIds.includes(
												favorite.course_id,
											)}
											onToggleFavorite={() =>
												toggleFavorite(favorite.course_id)
											}
										/>
									</div>
								</article>
							))}
						</div>
					)}
				</section>
			)}
		</main>
	);
}

export default MyCoursesPage;
