from app.config import settings
from app.errors import (
    CourseNotFoundError,
    EmailAlreadyRegisteredError,
    EnrollmentAlreadyExistsError,
    EnrollmentRequiredError,
    FavoriteAlreadyExistsError,
    InvalidCredentialsError,
    InvalidTokenError,
    LessonNotFoundError,
    ReviewAlreadyExistsError,
    ReviewEnrollmentRequiredError,
    SearchQueryTooShortError,
)
from app.models import Course, Lesson, User
from app.repositories import (
    CourseRepository,
    EnrollmentRepository,
    FavoriteRepository,
    LessonRepository,
    ProgressRepository,
    ReviewRepository,
    UserRepository,
)
from app.schemas import (
    AdminStatsRead,
    CourseCreate,
    CourseLevel,
    CourseProgressRead,
    CourseUpdate,
    EnrollmentRead,
    FavoriteRead,
    LessonCreate,
    LessonProgressRead,
    ReviewCreate,
    ReviewRead,
    TokenRead,
    UserCreate,
    UserLogin,
)
from app.security import (
    create_access_token,
    decode_access_token,
    hash_password,
    verify_password,
)
from app.slugs import make_course_slug

MIN_SEARCH_QUERY_LENGTH = 2


class CourseService:
    def __init__(self, repository: CourseRepository) -> None:
        self.repository = repository

    async def _generate_unique_slug(self, title: str) -> str:
        base_slug = make_course_slug(title)

        candidate = base_slug
        counter = 2
        while await self.repository.get_by_slug(candidate) is not None:
            suffix = f"-{counter}"
            stem = base_slug[: 60 - len(suffix)].rstrip("-")
            candidate = f"{stem}{suffix}"
            counter += 1
        return candidate

    async def list_courses(
        self,
        *,
        level: CourseLevel | None = None,
        q: str | None = None,
    ) -> list[Course]:
        if q is not None:
            q = q.strip().lower()
            if len(q) < MIN_SEARCH_QUERY_LENGTH:
                raise SearchQueryTooShortError(MIN_SEARCH_QUERY_LENGTH)
        return await self.repository.list_courses(level=level, q=q)

    async def get_course(self, course_id: int) -> Course:
        course = await self.repository.get_by_id(course_id)
        if not course:
            raise CourseNotFoundError()
        return course

    async def create_course(self, course_in: CourseCreate) -> Course:
        slug = await self._generate_unique_slug(course_in.title)
        return await self.repository.create(course_in, slug=slug)

    async def update_course(self, course_id: int, course_in: CourseUpdate) -> Course:
        course = await self.get_course(course_id)

        updates = course_in.model_dump(exclude_unset=True, exclude_none=True)
        if not updates:
            return course
        return await self.repository.update(course, updates)


class LessonService:
    def __init__(
        self,
        course_repository: CourseRepository,
        lesson_repository: LessonRepository,
    ) -> None:
        self.course_repository = course_repository
        self.lesson_repository = lesson_repository

    async def list_course_lessons(self, course_id: int) -> list[Lesson]:
        await self._ensure_course_exists(course_id)
        return await self.lesson_repository.list_by_course(course_id)

    async def create_course_lesson(
        self, course_id: int, lesson_in: LessonCreate
    ) -> Lesson:
        await self._ensure_course_exists(course_id)
        return await self.lesson_repository.create(course_id, lesson_in)

    async def _ensure_course_exists(self, course_id: int) -> None:
        course = await self.course_repository.get_by_id(course_id)
        if not course:
            raise CourseNotFoundError()


class UserService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    async def register_user(self, user_in: UserCreate) -> User:
        existing_user = await self.repository.get_by_email(user_in.email)
        if existing_user is not None:
            raise EmailAlreadyRegisteredError()
        return await self.repository.create(user_in, hash_password(user_in.password))

    async def authenticate_user(self, login_in: UserLogin) -> User:
        user = await self.repository.get_by_email(login_in.email)
        if user is None or not verify_password(login_in.password, user.hashed_password):
            raise InvalidCredentialsError()
        return user

    async def get_by_id(self, user_id: int) -> User:
        user = await self.repository.get_by_id(user_id)
        if user is None:
            raise InvalidTokenError()
        return user


class AuthService:
    def __init__(self, user_service: UserService) -> None:
        self.user_service = user_service

    async def login(self, login_in: UserLogin) -> TokenRead:
        user = await self.user_service.authenticate_user(login_in)
        token = create_access_token(
            subject=str(user.id),
            secret_key=settings.secret_key,
            expires_in_seconds=settings.access_token_expire_minutes * 60,
        )
        return TokenRead(access_token=token)

    async def get_current_user(self, token: str) -> User:
        payload = decode_access_token(token, secret_key=settings.secret_key)
        if payload is None:
            raise InvalidTokenError()

        subject = payload.get("sub")
        if not isinstance(subject, str) or not subject.isdigit():
            raise InvalidTokenError()

        return await self.user_service.get_by_id(int(subject))


class LearningService:
    def __init__(
        self,
        course_repository: CourseRepository,
        lesson_repository: LessonRepository,
        enrollment_repository: EnrollmentRepository,
        progress_repository: ProgressRepository,
        favorite_repository: FavoriteRepository,
    ) -> None:
        self.course_repository = course_repository
        self.lesson_repository = lesson_repository
        self.enrollment_repository = enrollment_repository
        self.progress_repository = progress_repository
        self.favorite_repository = favorite_repository

    async def enroll(self, *, course_id: int, user: User) -> EnrollmentRead:
        course = await self._get_course(course_id=course_id)

        existing_enrollment = await self.enrollment_repository.get(
            user_id=user.id, course_id=course_id
        )
        if existing_enrollment is not None:
            raise EnrollmentAlreadyExistsError()

        enrollment = await self.enrollment_repository.create(
            user_id=user.id, course_id=course_id
        )

        return EnrollmentRead(
            id=enrollment.id,
            user_id=user.id,
            course_id=course.id,
            course_title=course.title,
        )

    async def list_my_enrollments(self, user: User) -> list[EnrollmentRead]:
        rows = await self.enrollment_repository.list_with_courses_by_user(user.id)
        return [
            EnrollmentRead(
                id=e.id,
                user_id=user.id,
                course_id=c.id,
                course_title=c.title,
            )
            for e, c in rows
        ]

    async def complete_lesson(
        self, *, lesson_id: int, user: User
    ) -> LessonProgressRead:
        lesson = await self.lesson_repository.get_by_id(lesson_id=lesson_id)
        if lesson is None:
            raise LessonNotFoundError()

        enrollment = await self.enrollment_repository.get(
            user_id=user.id, course_id=lesson.course_id
        )
        if enrollment is None:
            raise EnrollmentRequiredError()

        progress = await self.progress_repository.get(
            user_id=user.id, lesson_id=lesson_id
        )
        if progress is None:
            progress = await self.progress_repository.create_completed(
                user_id=user.id, lesson_id=lesson_id
            )

        return LessonProgressRead(
            lesson_id=lesson.id,
            course_id=lesson.course_id,
            completed=progress.completed,
        )

    async def list_my_progress(self, user: User) -> list[CourseProgressRead]:
        rows = await self.enrollment_repository.list_with_courses_by_user(user.id)

        result: list[CourseProgressRead] = []
        for _, course in rows:
            total_lessons = await self.lesson_repository.count_by_course(
                course_id=course.id
            )
            completed_lessons = (
                await self.progress_repository.list_completed_lesson_ids_by_course(
                    user_id=user.id, course_id=course.id
                )
            )
            percent = (
                round((len(completed_lessons) / total_lessons * 100), 1)
                if total_lessons
                else 0.0
            )
            result.append(
                CourseProgressRead(
                    course_id=course.id,
                    course_title=course.title,
                    completed_lessons=len(completed_lessons),
                    completed_lesson_ids=completed_lessons,
                    total_lessons=total_lessons,
                    percent=percent,
                )
            )
        return result

    async def favorite_course(self, *, course_id: int, user: User) -> FavoriteRead:
        course = await self._get_course(course_id)

        existing_favorite = await self.favorite_repository.get(
            user_id=user.id, course_id=course_id
        )
        if existing_favorite is not None:
            raise FavoriteAlreadyExistsError()

        favorite = await self.favorite_repository.create(
            user_id=user.id, course_id=course_id
        )
        return FavoriteRead(
            id=favorite.id,
            user_id=user.id,
            course_id=course.id,
            course_title=course.title,
        )

    async def list_my_favorites(self, user: User) -> list[FavoriteRead]:
        favorites = await self.favorite_repository.list_with_courses_by_user(
            user_id=user.id
        )
        return [
            FavoriteRead(
                id=favorite.id,
                user_id=user.id,
                course_id=course.id,
                course_title=course.title,
            )
            for favorite, course in favorites
        ]

    async def remove_favorite_course(self, *, course_id: int, user: User) -> None:
        await self.favorite_repository.delete(user_id=user.id, course_id=course_id)

    async def _get_course(self, course_id: int) -> Course:
        course = await self.course_repository.get_by_id(course_id=course_id)
        if course is None:
            raise CourseNotFoundError()
        return course


class AdminService:
    def __init__(
        self,
        course_repository: CourseRepository,
        lesson_repository: LessonRepository,
        user_repository: UserRepository,
        enrollment_repository: EnrollmentRepository,
        progress_repository: ProgressRepository,
        favorite_repository: FavoriteRepository,
        review_repository: ReviewRepository,
    ) -> None:
        self.course_repository = course_repository
        self.lesson_repository = lesson_repository
        self.user_repository = user_repository
        self.enrollment_repository = enrollment_repository
        self.progress_repository = progress_repository
        self.favorite_repository = favorite_repository
        self.review_repository = review_repository

    async def get_stats(self) -> AdminStatsRead:
        return AdminStatsRead(
            courses=await self.course_repository.count(),
            lessons=await self.lesson_repository.count(),
            users=await self.user_repository.count(),
            enrollments=await self.enrollment_repository.count(),
            completed_lessons=await self.progress_repository.count_completed(),
            favorite_courses=await self.favorite_repository.count(),
            reviews=await self.review_repository.count(),
        )


class ReviewService:
    def __init__(
        self,
        course_repository: CourseRepository,
        enrollment_repository: EnrollmentRepository,
        review_repository: ReviewRepository,
    ) -> None:
        self.course_repository = course_repository
        self.enrollment_repository = enrollment_repository
        self.review_repository = review_repository

    async def create_review(
        self, *, course_id: int, user: User, review_in: ReviewCreate
    ) -> ReviewRead:
        course = await self.course_repository.get_by_id(course_id)
        if course is None:
            raise CourseNotFoundError()

        enrollment = await self.enrollment_repository.get(
            user_id=user.id, course_id=course_id
        )
        if enrollment is None:
            raise ReviewEnrollmentRequiredError()

        existing_review = await self.review_repository.get(
            user_id=user.id, course_id=course_id
        )
        if existing_review is not None:
            raise ReviewAlreadyExistsError()

        review = await self.review_repository.create(
            user_id=user.id, course_id=course_id, review_in=review_in
        )
        return ReviewRead(
            id=review.id,
            course_id=review.course_id,
            user_id=review.user_id,
            rating=review.rating,
            comment=review.comment,
        )

    async def list_course_reviews(self, course_id: int) -> list[ReviewRead]:
        course = await self.course_repository.get_by_id(course_id)
        if course is None:
            raise CourseNotFoundError()

        reviews = await self.review_repository.list_by_course(course_id=course_id)
        return [
            ReviewRead(
                id=review.id,
                course_id=review.course_id,
                user_id=review.user_id,
                rating=review.rating,
                comment=review.comment,
            )
            for review in reviews
        ]
