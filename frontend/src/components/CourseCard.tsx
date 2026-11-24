import { Link, useLocation } from "react-router";

import type { Course } from "../types/course";
import FavoriteButton from "./FavoriteButton";

const levelLabels = {
	beginner: "Начальный",
	intermediate: "Средний",
	advanced: "Продвинутый",
};

type CourseCardProps = {
	course: Course;
	isFavorite: boolean;
	isFavoritePending: boolean;
	onToggleFavorite?: () => void;
};

function CourseCard({
	course,
	isFavorite,
	isFavoritePending,
	onToggleFavorite,
}: CourseCardProps) {
	const location = useLocation();

	return (
		<article className="course-card">
			<div className="course-card-top">
				<span className={"course-level course-level--" + course.level}>
					{levelLabels[course.level]}
				</span>
				{onToggleFavorite && (
					<FavoriteButton
						title={course.title}
						isFavorite={isFavorite}
						isFavoritePending={isFavoritePending}
						onToggleFavorite={onToggleFavorite}
					/>
				)}
			</div>
			{onToggleFavorite && (
				<span className="favorite-hint" aria-hidden="true">
					{isFavorite ? "Убрать из избранного" : "Добавить в избранное"}
				</span>
			)}
			<h2>
				<Link
					to={`/courses/${course.id}`}
					state={{ from: location.pathname + location.search }}
				>
					{course.title}
				</Link>
			</h2>
			<p className="course-price">
				{course.price === 0
					? "Бесплатно"
					: course.price.toLocaleString("ru-RU") + " ₽"}
			</p>
		</article>
	);
}

export default CourseCard;
