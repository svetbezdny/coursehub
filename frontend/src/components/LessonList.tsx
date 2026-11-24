import type { Lesson } from "../types/lesson";

type LessonListProps = {
	lessons: Lesson[];
	showProgress: boolean;
	completedLessonIds: number[];
	completingLessonId: number | null;
	onCompleteLesson: (lessonId: number) => void;
};

function LessonList({
	lessons,
	showProgress,
	completedLessonIds,
	completingLessonId,
	onCompleteLesson,
}: LessonListProps) {
	return lessons.length === 0 ? (
		<p>Уроков пока нет</p>
	) : (
		<ol>
			{lessons.map((lesson) => (
				<li key={lesson.id}>
					<div className="lesson-row">
						<span>{lesson.title}</span>
						{showProgress &&
							(completedLessonIds.includes(lesson.id) ? (
								<span className="lesson-completed">✓ Завершён</span>
							) : (
								<button
									type="button"
									className="secondary-button"
									disabled={completingLessonId !== null}
									onClick={() => onCompleteLesson(lesson.id)}
								>
									{completingLessonId === lesson.id
										? "Сохраняем…"
										: "Завершить"}
								</button>
							))}
					</div>
				</li>
			))}
		</ol>
	);
}

export default LessonList;
