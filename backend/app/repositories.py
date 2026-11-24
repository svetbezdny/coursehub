from typing import Any

from sqlalchemy import delete, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Course, Enrollment, FavoriteCourse, Lesson, LessonProgress, User
from app.schemas import CourseCreate, LessonCreate, UserCreate


class CourseRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_courses(
        self, *, level: str | None = None, q: str | None = None
    ) -> list[Course]:
        stmt = select(Course).order_by(Course.id)

        if level is not None:
            stmt = stmt.where(Course.level == level)

        if q is not None:
            stmt = stmt.where(func.lower(Course.title).contains(q, autoescape=True))

        result = await self.session.scalars(stmt)
        return list(result)

    async def get_by_id(self, course_id: int) -> Course | None:
        return await self.session.get(Course, course_id)

    async def get_by_slug(self, slug: str) -> Course | None:
        result = await self.session.scalars(select(Course).where(Course.slug == slug))
        return result.first()

    async def create(self, course_in: CourseCreate, *, slug: str) -> Course:
        course = Course(**course_in.model_dump(), slug=slug)
        self.session.add(course)
        await self.session.commit()
        await self.session.refresh(course)
        return course

    async def update(self, course: Course, updates: dict[str, Any]) -> Course:
        for k, v in updates.items():
            setattr(course, k, v)

        await self.session.commit()
        await self.session.refresh(course)
        return course


class LessonRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def list_by_course(self, course_id: int) -> list[Lesson]:
        stmt = (
            select(Lesson)
            .where(Lesson.course_id == course_id)
            .order_by(Lesson.order, Lesson.id)
        )
        result = await self.session.scalars(stmt)
        return list(result)

    async def create(self, course_id: int, lesson_in: LessonCreate) -> Lesson:
        order = lesson_in.order
        if not order:
            max_order = await self.session.scalar(
                select(func.max(Lesson.order)).where(Lesson.course_id == course_id)
            )
            order = int(max_order or 0) + 1

        lesson = Lesson(course_id=course_id, title=lesson_in.title, order=order)
        self.session.add(lesson)
        await self.session.commit()
        await self.session.refresh(lesson)
        return lesson

    async def get_by_id(self, lesson_id: int) -> Lesson | None:
        return await self.session.get(Lesson, lesson_id)

    async def count_by_course(self, course_id: int) -> int:
        stmt = select(func.count(Lesson.id)).where(Lesson.course_id == course_id)
        return int(await self.session.scalar(stmt) or 0)


class UserRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get_by_email(self, email: str) -> User | None:
        result = await self.session.scalar(
            select(User).where(func.lower(User.email) == email.lower())
        )
        return result

    async def get_by_id(self, user_id: int) -> User | None:
        return await self.session.get(User, user_id)

    async def create(self, user_in: UserCreate, hashed_password: str) -> User:
        user = User(
            email=user_in.email.lower(),
            full_name=user_in.full_name,
            role="student",
            hashed_password=hashed_password,
        )
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user


class EnrollmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, *, user_id: int, course_id: int) -> Enrollment | None:
        stmt = select(Enrollment).where(
            Enrollment.user_id == user_id,
            Enrollment.course_id == course_id,
        )
        return await self.session.scalar(stmt)

    async def create(self, *, user_id: int, course_id: int) -> Enrollment:
        enrollment = Enrollment(user_id=user_id, course_id=course_id)
        self.session.add(enrollment)
        await self.session.commit()
        await self.session.refresh(enrollment)
        return enrollment

    async def list_with_courses_by_user(
        self, user_id: int
    ) -> list[tuple[Enrollment, Course]]:
        stmt = (
            select(Enrollment, Course)
            .join(Course, Enrollment.course_id == Course.id)
            .where(Enrollment.user_id == user_id)
            .order_by(Enrollment.id)
        )
        result = await self.session.execute(stmt)
        return [(e, c) for e, c in result.all()]


class ProgressRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, *, user_id: int, lesson_id: int) -> LessonProgress | None:
        stmt = select(LessonProgress).where(
            LessonProgress.user_id == user_id, LessonProgress.lesson_id == lesson_id
        )
        return await self.session.scalar(stmt)

    async def create_completed(self, *, user_id: int, lesson_id: int) -> LessonProgress:
        progress = LessonProgress(
            user_id=user_id,
            lesson_id=lesson_id,
            completed=True,
        )
        self.session.add(progress)
        await self.session.commit()
        await self.session.refresh(progress)
        return progress

    async def list_completed_lesson_ids_by_course(
        self, *, user_id: int, course_id: int
    ) -> list[int]:
        stmt = (
            select(LessonProgress.lesson_id)
            .join(Lesson, Lesson.id == LessonProgress.lesson_id)
            .where(
                LessonProgress.user_id == user_id,
                LessonProgress.completed.is_(True),
                Lesson.course_id == course_id,
            )
        )
        result = await self.session.scalars(stmt)
        return list(result)


class FavoriteRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, *, user_id: int, course_id: int) -> FavoriteCourse | None:
        stmt = select(FavoriteCourse).where(
            FavoriteCourse.user_id == user_id, FavoriteCourse.course_id == course_id
        )
        return await self.session.scalar(stmt)

    async def list_with_courses_by_user(
        self, *, user_id: int
    ) -> list[tuple[FavoriteCourse, Course]]:
        stmt = (
            select(FavoriteCourse, Course)
            .join(Course, FavoriteCourse.course_id == Course.id)
            .where(FavoriteCourse.user_id == user_id)
            .order_by(FavoriteCourse.id, Course.id)
        )
        result = await self.session.execute(stmt)
        return [(f, c) for f, c in result.all()]

    async def create(self, *, user_id: int, course_id: int) -> FavoriteCourse:
        favorite = FavoriteCourse(user_id=user_id, course_id=course_id)
        self.session.add(favorite)
        await self.session.commit()
        await self.session.refresh(favorite)
        return favorite

    async def delete(self, user_id: int, course_id: int) -> None:
        stmt = delete(FavoriteCourse).where(
            FavoriteCourse.user_id == user_id, FavoriteCourse.course_id == course_id
        )
        await self.session.execute(stmt)
        await self.session.commit()
