import { createContext } from "react";

import type { Enrollment } from "../types/enrollment";

export type EnrollmentsContextValue = {
	enrollments: Enrollment[];
	isLoading: boolean;
	error: string | null;
	refresh: () => Promise<void>;
	addEnrollment: (enrollment: Enrollment) => void;
};

export const EnrollmentsContext = createContext<
	EnrollmentsContextValue | undefined
>(undefined);
