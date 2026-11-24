import type { SubmitEvent } from "react";
import { useState } from "react";
import { Link, Navigate, useNavigate } from "react-router";

import { createCourse } from "../api/courses";
import { ApiError } from "../api/errors";
import { useAuth } from "../auth/useAuth";
import type { Course } from "../types/course";

function CreateCoursePage() {
	const { user, token, signOut } = useAuth();
	const navigate = useNavigate();

	const [title, setTitle] = useState("");
	const [level, setLevel] = useState<Course["level"]>("beginner");
	const [price, setPrice] = useState("0.00");

	const [error, setError] = useState<string | null>(null);
	const [isSubmitting, setIsSubmitting] = useState(false);

	async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
		event.preventDefault();

		if (isSubmitting) return;
		if (!token) {
			signOut();
			return;
		}
		setError(null);
		setIsSubmitting(true);

		try {
			const course = await createCourse(
				{ title: title.trim(), level, price },
				token,
			);
			navigate(`/courses/${course.id}`, { replace: true });
		} catch (error) {
			if (error instanceof ApiError && error.status === 401) {
				signOut();
				return;
			} else {
				setError(
					error instanceof Error ? error.message : "Ошибка создания курса",
				);
			}
		} finally {
			setIsSubmitting(false);
		}
	}

	if (!user) {
		return <Navigate to="/login" replace />;
	}

	if (user.role !== "admin" && user.role !== "author") {
		return (
			<main className="page">
				<h1>Недостаточно прав</h1>
				<p>Создавать курсы могут только авторы и администраторы</p>
				<Link to="/">На главную</Link>
			</main>
		);
	}

	return (
		<main className="page">
			<h1>Создание курса</h1>
			<Link to={"/"} className="back-link">
				На главную
			</Link>
			<form className="auth-form" onSubmit={handleSubmit}>
				<label>
					Название
					<input
						type="text"
						name="title"
						minLength={3}
						maxLength={80}
						value={title}
						onChange={(e) => setTitle(e.target.value)}
						required
					/>
				</label>
				<label>
					Уровень
					<select
						name="level"
						value={level}
						onChange={(e) => {
							const value = e.target.value;
							if (
								value === "beginner" ||
								value === "intermediate" ||
								value === "advanced"
							) {
								setLevel(value);
							}
						}}
					>
						<option value="beginner">Начальный</option>
						<option value="intermediate">Средний</option>
						<option value="advanced">Продвинутый</option>
					</select>
				</label>
				<label>
					Цена, ₽
					<input
						type="number"
						name="price"
						min="0"
						max="99999999.99"
						step="0.01"
						value={price}
						onChange={(e) => setPrice(e.target.value)}
						required
					/>
				</label>
				{error && <p role="alert">{error}</p>}
				<button
					type="submit"
					className="primary-button"
					disabled={isSubmitting}
				>
					{isSubmitting ? "Создание курса..." : "Создать курс"}
				</button>
			</form>
		</main>
	);
}

export default CreateCoursePage;
