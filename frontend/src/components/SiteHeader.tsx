import { Link } from "react-router";

import AuthActions from "./AuthActions";

function SiteHeader() {
	return (
		<header className="site-header">
			<div className="site-header-inner">
				<Link to={"/"} className="site-brand">
					CourseHub
				</Link>
				<AuthActions />
			</div>
		</header>
	);
}

export default SiteHeader;
