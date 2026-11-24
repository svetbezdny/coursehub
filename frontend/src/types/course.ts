export type Course = {
	id: number;
	title: string;
	slug: string;
	level: "beginner" | "intermediate" | "advanced";
	price: number;
};

export type CourseCreate = {
	title: string;
	level: Course["level"];
	price: string;
};

export type FavoriteCourse = {
	id: number;
	user_id: number;
	course_id: number;
	course_title: string;
};
