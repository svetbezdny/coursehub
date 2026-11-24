import { Link } from "react-router";

function NotFoundPage() {
	return (
		<main className="page">
			<h1>Страница не найдена</h1>
			<p>Проверьте адрес или вернитесь в каталог</p>
			<Link to={"/"}>К каталогу</Link>
		</main>
	);
}

export default NotFoundPage;
