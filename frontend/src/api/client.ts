import { ApiError } from "./errors";

type ApiFetchOptions = RequestInit & {
	token?: string;
	errorMessage: string;
	errorMessages?: Partial<Record<number, string>>;
	errorDetails?: Record<string, string>;
};

export async function apiFetch(
	path: string,
	{
		token,
		errorMessage,
		errorMessages,
		errorDetails,
		...init
	}: ApiFetchOptions,
): Promise<Response> {
	const headers = new Headers(init.headers);

	if (token) {
		headers.set("Authorization", `Bearer ${token}`);
	}

	const response = await fetch(path, { ...init, headers });
	if (!response.ok) {
		let message = errorMessages?.[response.status] ?? errorMessage;

		if (response.status === 400 && errorDetails) {
			const body: unknown = await response.json().catch(() => null);

			if (
				typeof body === "object" &&
				body !== null &&
				"detail" in body &&
				typeof body.detail === "string" &&
				Object.hasOwn(errorDetails, body.detail)
			) {
				message = errorDetails[body.detail];
			}
		}

		throw new ApiError(message, response.status);
	}

	return response;
}
