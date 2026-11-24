import type { ReactNode } from "react";
import { useCallback, useEffect, useRef, useState } from "react";

import { ApiError } from "../api/errors";
import { getMyEnrollments } from "../api/learning";
import { useAuth } from "../auth/useAuth";
import type { Enrollment } from "../types/enrollment";
import { EnrollmentsContext } from "./EnrollmentsContext";

type EnrollmentsProviderProps = {
	children: ReactNode;
};

function EnrollmentsProvider({ children }: EnrollmentsProviderProps) {
	const { token, signOut } = useAuth();

	const [enrollments, setEnrollments] = useState<Enrollment[]>([]);
	const [isLoading, setIsLoading] = useState(Boolean(token));
	const [error, setError] = useState<string | null>(null);

	const requestVersion = useRef(0);
	const lastUpdatedAt = useRef(0);

	const refresh = useCallback(() => {
		const version = ++requestVersion.current;

		if (!token) {
			return Promise.resolve();
		}

		return getMyEnrollments(token)
			.then((data) => {
				if (version === requestVersion.current) {
					setEnrollments(data);
					lastUpdatedAt.current = Date.now();
					setError(null);
				}
			})
			.catch((error: unknown) => {
				if (version !== requestVersion.current) return;
				else if (error instanceof ApiError && error.status === 401) signOut();
				else
					setError(
						error instanceof Error ? error.message : "Ошибка обновления курсов",
					);
			})
			.finally(() => {
				if (version === requestVersion.current) setIsLoading(false);
			});
	}, [token, signOut]);

	const invalidateRequests = useCallback(() => {
		requestVersion.current++;
	}, []);

	useEffect(() => {
		refresh();
		return invalidateRequests;
	}, [refresh, invalidateRequests]);

	useEffect(() => {
		function handleVisibilityChange() {
			if (
				token &&
				document.visibilityState === "visible" &&
				Date.now() - lastUpdatedAt.current >= 60_000
			) {
				refresh();
			}
		}
		document.addEventListener("visibilitychange", handleVisibilityChange);
		return () => {
			document.removeEventListener("visibilitychange", handleVisibilityChange);
		};
	}, [token, refresh]);

	function addEnrollment(enrollment: Enrollment) {
		requestVersion.current++;
		setIsLoading(false);
		setError(null);

		setEnrollments((current) => {
			if (current.some((item) => item.course_id === enrollment.course_id)) {
				return current;
			}
			return [...current, enrollment];
		});
	}

	return (
		<EnrollmentsContext.Provider
			value={{ enrollments, isLoading, error, refresh, addEnrollment }}
		>
			{children}
		</EnrollmentsContext.Provider>
	);
}

export default EnrollmentsProvider;
