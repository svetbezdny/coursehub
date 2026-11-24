import type {
	LoginData,
	RegisterData,
	TokenResponse,
	User,
} from "../types/auth";
import { apiFetch } from "./client";

export async function login(data: LoginData): Promise<TokenResponse> {
	const response = await apiFetch("/api/auth/login", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(data),
		errorMessage: "Не удалось выполнить вход",
		errorMessages: { 401: "Неверный email или пароль" },
	});

	return response.json();
}

export async function getCurrentUser(token: string): Promise<User> {
	const response = await apiFetch("/api/users/me", {
		token,
		errorMessage: "Не удалось загрузить пользователя",
		errorMessages: { 401: "Сессия истекла. Войдите снова" },
	});

	return response.json();
}

export async function register(data: RegisterData): Promise<User> {
	const response = await apiFetch("/api/auth/register", {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify(data),
		errorMessage: "Не удалось зарегистрироваться",
		errorDetails: {
			"Email already registered": "Этот email уже зарегистрирован",
		},
	});

	return response.json();
}
