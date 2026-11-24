import { useEffect, useState } from "react";

import { ApiError } from "../api/errors";
import {
	addFavoriteCourse,
	getMyFavorites,
	removeFavoriteCourse,
} from "../api/learning";
import { useAuth } from "../auth/useAuth";
import type { FavoriteCourse } from "../types/course";

export function useFavorites() {
	const { token, signOut } = useAuth();

	const [favorites, setFavorites] = useState<FavoriteCourse[] | null>(null);
	const favoriteIds = favorites?.map((favorite) => favorite.course_id) ?? null;

	const [favoritesError, setFavoritesError] = useState<string | null>(null);
	const [pendingFavoriteIds, setPendingFavoriteIds] = useState<number[]>([]);

	useEffect(() => {
		if (!token) return;

		let ignore = false;

		getMyFavorites(token)
			.then((favorites) => {
				if (ignore) return;

				setFavorites(favorites);
				setFavoritesError(null);
			})
			.catch((error: unknown) => {
				if (ignore) return;

				if (error instanceof ApiError && error.status === 401) {
					signOut();
					return;
				}

				setFavoritesError("Не удалось загрузить избранное");
			});
		return () => {
			ignore = true;
		};
	}, [token, signOut]);

	async function toggleFavorite(courseId: number) {
		if (
			!token ||
			favoriteIds === null ||
			pendingFavoriteIds.includes(courseId)
		) {
			return;
		}

		const isFavorite = favoriteIds.includes(courseId);
		setFavoritesError(null);
		setPendingFavoriteIds((ids) => [...ids, courseId]);

		try {
			if (isFavorite) {
				await removeFavoriteCourse(courseId, token);
				setFavorites(
					(current) =>
						current?.filter((favorite) => favorite.course_id !== courseId) ??
						null,
				);
			} else {
				const favorite = await addFavoriteCourse(courseId, token);
				setFavorites((current) =>
					current === null ? null : [...current, favorite],
				);
			}
		} catch (error) {
			if (error instanceof ApiError && error.status === 401) {
				signOut();
				return;
			}

			setFavoritesError(
				error instanceof Error
					? error.message
					: "Не удалось обновить избранное",
			);
		} finally {
			setPendingFavoriteIds((ids) => ids.filter((id) => id !== courseId));
		}
	}

	return {
		favorites,
		favoriteIds,
		favoritesError,
		pendingFavoriteIds,
		toggleFavorite,
	};
}
