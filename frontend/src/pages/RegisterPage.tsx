import type { SubmitEvent } from "react";
import { useState } from "react";
import { Link, Navigate, useLocation, useNavigate } from "react-router";

import { register } from "../api/auth";
import { useAuth } from "../auth/useAuth";

function RegisterPage() {
	const [fullName, setFullName] = useState("");
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");

	const [error, setError] = useState<string | null>(null);
	const [isSubmitting, setIsSubmitting] = useState(false);

	const { user } = useAuth();

	const navigate = useNavigate();
	const location = useLocation();

	async function handleSubmit(event: SubmitEvent<HTMLFormElement>) {
		event.preventDefault();
		if (isSubmitting) return;
		setError(null);
		setIsSubmitting(true);

		try {
			await register({
				email: email.trim(),
				password: password,
				full_name: fullName.trim() || null,
			});
			navigate("/login", {
				replace: true,
				state: {
					registered: true,
					returnTo: location.state?.returnTo,
					returnState: location.state?.returnState,
				},
			});
		} catch (error) {
			setError(error instanceof Error ? error.message : "Ошибка регистрации");
		} finally {
			setIsSubmitting(false);
		}
	}

	if (user) {
		return <Navigate to="/" replace />;
	}

	return (
		<main className="page">
			<Link to={"/"}>К каталогу</Link>
			<h1>Регистрация</h1>
			<form className="auth-form" onSubmit={handleSubmit}>
				<label>
					Имя
					<input
						type="text"
						name="full_name"
						autoComplete="name"
						maxLength={120}
						value={fullName}
						onChange={(e) => setFullName(e.target.value)}
					/>
				</label>
				<label>
					Email
					<input
						type="email"
						name="email"
						autoComplete="email"
						maxLength={120}
						required
						value={email}
						onChange={(e) => setEmail(e.target.value)}
					/>
				</label>
				<label>
					Пароль
					<input
						type="password"
						name="password"
						autoComplete="new-password"
						minLength={8}
						maxLength={128}
						required
						value={password}
						onChange={(e) => setPassword(e.target.value)}
					/>
				</label>
				{error && <p role="alert">{error}</p>}
				<button
					className="primary-button"
					type="submit"
					disabled={isSubmitting}
				>
					{isSubmitting ? "Идет регистрация..." : "Зарегистрироваться"}
				</button>
			</form>
			<p>
				Есть аккаунт?{" "}
				<Link to="/login" state={location.state}>
					Войти
				</Link>
			</p>
		</main>
	);
}

export default RegisterPage;
