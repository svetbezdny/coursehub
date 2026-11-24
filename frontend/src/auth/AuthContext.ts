import { createContext } from "react";

import type { User } from "../types/auth";

export type AuthContextValue = {
	user: User | null;
	token: string | null;
	signIn: (token: string, user: User) => void;
	signOut: () => void;
	isInitializing: boolean;
};

export const AuthContext = createContext<AuthContextValue | undefined>(
	undefined,
);
