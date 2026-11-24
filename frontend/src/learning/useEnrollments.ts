import { useContext } from "react";

import { EnrollmentsContext } from "./EnrollmentsContext";

export function useEnrollments() {
	const context = useContext(EnrollmentsContext);
	if (context === undefined) {
		throw new Error(
			"useEnrollments должен использоваться внутри EnrollmentsProvider",
		);
	}
	return context;
}
