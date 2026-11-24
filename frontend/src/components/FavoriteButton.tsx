type FavoriteButtonProps = {
	title: string;
	isFavorite: boolean;
	isFavoritePending: boolean;
	onToggleFavorite: () => void;
};

function FavoriteButton({
	title,
	isFavorite,
	isFavoritePending,
	onToggleFavorite,
}: FavoriteButtonProps) {
	return (
		<button
			type="button"
			className="favorite-button"
			aria-label={`Избранное: ${title}`}
			aria-pressed={isFavorite}
			disabled={isFavoritePending}
			onClick={onToggleFavorite}
		>
			{isFavorite ? "★" : "☆"}
		</button>
	);
}

export default FavoriteButton;
