export type Lesson = {
	id: number;
	course_id: number;
	title: string;
	order: number;
};

export type LessonProgress = {
	lesson_id: number;
	course_id: number;
	completed: boolean;
};

export type CourseProgress = {
	course_id: number;
	course_title: string;
	completed_lessons: number;
	completed_lesson_ids: number[];
	total_lessons: number;
	percent: number;
};
