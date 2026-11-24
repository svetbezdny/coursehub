export type User = {
	id: number;
	email: string;
	full_name: string | null;
	role: "student" | "author" | "admin";
};

export type LoginData = {
	email: string;
	password: string;
};

export type TokenResponse = {
	access_token: string;
	token_type: string;
};

export type RegisterData = {
	email: string;
	password: string;
	full_name: string | null;
};
