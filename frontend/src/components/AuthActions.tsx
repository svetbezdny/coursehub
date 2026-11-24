import { Link, useLocation } from "react-router";

import { useAuth } from "../auth/useAuth";

function AuthActions() {
	const { user, signOut } = useAuth();

	const location = useLocation();
	const isAuthPage =
		location.pathname === "/login" || location.pathname === "/register";

	return (
		<div className="auth-actions">
			{user ? (
				<>
					<Link to={"/my-courses"} title="Мои курсы">
						{user.full_name || user.email}
					</Link>
					<button className="secondary-button" type="button" onClick={signOut}>
						Выйти
					</button>
				</>
			) : (
				<Link
					to={"/login"}
					state={
						isAuthPage
							? location.state
							: {
									returnTo: location.pathname + location.search,
									returnState: location.state,
								}
					}
				>
					Войти
				</Link>
			)}
		</div>
	);
}

export default AuthActions;
