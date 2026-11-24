import type { ReactNode } from "react";
import { useCallback, useEffect, useRef, useState } from "react";

import { getCurrentUser } from "../api/auth";
import { ApiError } from "../api/errors";
import type { User } from "../types/auth";
import { AuthContext } from "./AuthContext";

type AuthProviderProps = {
	children: ReactNode;
};

function AuthProvider({ children }: AuthProviderProps) {
	const [user, setUser] = useState<User | null>(null);
	const [token, setToken] = useState<string | null>(null);
	const [isInitializing, setIsInitializing] = useState(true);

	const authVersion = useRef(0);

	useEffect(() => {
		let ignore = false;

		async function restoreSession() {
			const version = ++authVersion.current;
			const savedToken = localStorage.getItem("access_token");

			try {
				if (savedToken === null) return;
				const user = await getCurrentUser(savedToken);

				if (
					!ignore &&
					version === authVersion.current &&
					localStorage.getItem("access_token") === savedToken
				) {
					setUser(user);
					setToken(savedToken);
				}
			} catch (error) {
				if (
					!ignore &&
					version === authVersion.current &&
					error instanceof ApiError &&
					error.status === 401 &&
					localStorage.getItem("access_token") === savedToken
				) {
					localStorage.removeItem("access_token");
					return;
				}
			} finally {
				if (!ignore && version === authVersion.current) {
					setIsInitializing(false);
				}
			}
		}

		function handleStorage(event: StorageEvent) {
			if (event.storageArea !== localStorage) return;
			if (event.key !== "access_token" && event.key !== null) return;
			authVersion.current++;
			setUser(null);
			setToken(null);

			const token = localStorage.getItem("access_token");
			if (!token) {
				setIsInitializing(false);
				return;
			}
			setIsInitializing(true);
			restoreSession();
		}

		window.addEventListener("storage", handleStorage);
		restoreSession();
		return () => {
			ignore = true;
			window.removeEventListener("storage", handleStorage);
		};
	}, []);

	function signIn(token: string, user: User) {
		authVersion.current++;
		localStorage.setItem("access_token", token);
		setUser(user);
		setToken(token);
		setIsInitializing(false);
	}

	const signOut = useCallback(() => {
		authVersion.current++;
		localStorage.removeItem("access_token");
		setUser(null);
		setToken(null);
		setIsInitializing(false);
	}, []);

	return (
		<AuthContext.Provider
			value={{ user, token, signIn, signOut, isInitializing }}
		>
			{children}
		</AuthContext.Provider>
	);
}

export default AuthProvider;
