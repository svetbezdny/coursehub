import type { SubmitEvent } from "react";
import { useState } from "react";
import { Link, Navigate, useLocation } from "react-router";

import { getCurrentUser, login } from "../api/auth";
import { useAuth } from "../auth/useAuth";

function LoginPage() {
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");

	const [error, setError] = useState<string | null>(null);
	const [isSubmitting, setIsSubmitting] = useState(false);

	const { signIn, user } = useAuth();

	const location = useLocation();

	async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
		event.preventDefault();
		if (isSubmitting) return;
		setError(null);
		setIsSubmitting(true);

		try {
			const tokenResponse = await login({ email: email.trim(), password });
			const user = await getCurrentUser(tokenResponse.access_token);
			signIn(tokenResponse.access_token, user);
		} catch (error) {
			setError(
				error instanceof Error ? error.message : "Ошибка получения токена",
			);
		} finally {
			setIsSubmitting(false);
		}
	}

	if (user) {
		return (
			<Navigate
				to={location.state?.returnTo ?? "/"}
				state={location.state?.returnState}
				replace
			/>
		);
	}

	return (
		<main className="page">
			<Link to={"/"}>К каталогу</Link>
			<h1>Вход</h1>
			{location.state?.registered === true && (
				<p role="status">Аккаунт создан. Войдите с вашим email и паролем</p>
			)}
			<form className="auth-form" onSubmit={handleSubmit}>
				<label>
					Email
					<input
						type="email"
						name="email"
						autoComplete="email"
						value={email}
						onChange={(e) => setEmail(e.target.value)}
						required
					/>
				</label>
				<label>
					Пароль
					<input
						type="password"
						name="password"
						autoComplete="current-password"
						value={password}
						onChange={(e) => setPassword(e.target.value)}
						required
					/>
				</label>
				{error && <p role="alert">{error}</p>}
				<button
					className="primary-button"
					type="submit"
					disabled={isSubmitting}
				>
					{isSubmitting ? "Входим…" : "Войти"}
				</button>
			</form>
			<p>
				Нет аккаунта?{" "}
				<Link to="/register" state={location.state}>
					Зарегистрироваться
				</Link>
			</p>
		</main>
	);
}

export default LoginPage;
