from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_session
from app.errors import InvalidTokenError, PermissionDeniedError
from app.models import User
from app.repositories import (
    CourseRepository,
    EnrollmentRepository,
    FavoriteRepository,
    LessonRepository,
    ProgressRepository,
    UserRepository,
)
from app.services import (
    AdminService,
    AuthService,
    CourseService,
    LearningService,
    LessonService,
    UserService,
)

bearer_scheme = HTTPBearer(auto_error=False)


def get_course_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> CourseRepository:
    return CourseRepository(session)


def get_course_service(
    repository: Annotated[CourseRepository, Depends(get_course_repository)],
) -> CourseService:
    return CourseService(repository)


def get_lesson_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> LessonRepository:
    return LessonRepository(session)


def get_lesson_service(
    course_repository: Annotated[CourseRepository, Depends(get_course_repository)],
    lesson_repository: Annotated[LessonRepository, Depends(get_lesson_repository)],
) -> LessonService:
    return LessonService(course_repository, lesson_repository)


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> UserRepository:
    return UserRepository(session)


def get_user_service(
    repository: Annotated[UserRepository, Depends(get_user_repository)],
) -> UserService:
    return UserService(repository)


def get_auth_service(
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> AuthService:
    return AuthService(user_service)


async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    service: Annotated[AuthService, Depends(get_auth_service)],
) -> User:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise InvalidTokenError()
    return await service.get_current_user(credentials.credentials)


async def require_author(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.role not in {"admin", "author"}:
        raise PermissionDeniedError()
    return current_user


async def require_admin(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.role != "admin":
        raise PermissionDeniedError()
    return current_user


def get_enrollment_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> EnrollmentRepository:
    return EnrollmentRepository(session)


def get_progress_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ProgressRepository:
    return ProgressRepository(session)


def get_favorite_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> FavoriteRepository:
    return FavoriteRepository(session)


def get_learning_service(
    course_repository: Annotated[CourseRepository, Depends(get_course_repository)],
    lesson_repository: Annotated[LessonRepository, Depends(get_lesson_repository)],
    enrollment_repository: Annotated[
        EnrollmentRepository, Depends(get_enrollment_repository)
    ],
    progress_repository: Annotated[
        ProgressRepository, Depends(get_progress_repository)
    ],
    favorite_repository: Annotated[
        FavoriteRepository, Depends(get_favorite_repository)
    ],
) -> LearningService:
    return LearningService(
        course_repository,
        lesson_repository,
        enrollment_repository,
        progress_repository,
        favorite_repository,
    )


def get_admin_service(
    course_repository: Annotated[CourseRepository, Depends(get_course_repository)],
    lesson_repository: Annotated[LessonRepository, Depends(get_lesson_repository)],
    user_repository: Annotated[UserRepository, Depends(get_user_repository)],
    enrollment_repository: Annotated[
        EnrollmentRepository, Depends(get_enrollment_repository)
    ],
    progress_repository: Annotated[
        ProgressRepository, Depends(get_progress_repository)
    ],
    favorite_repository: Annotated[
        FavoriteRepository, Depends(get_favorite_repository)
    ],
) -> AdminService:
    return AdminService(
        course_repository,
        lesson_repository,
        user_repository,
        enrollment_repository,
        progress_repository,
        favorite_repository,
    )


CourseServiceDep = Annotated[CourseService, Depends(get_course_service)]
LessonServiceDep = Annotated[LessonService, Depends(get_lesson_service)]
UserServiceDep = Annotated[UserService, Depends(get_user_service)]
AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]
CurrentUserDep = Annotated[User, Depends(get_current_user)]
LearningServiceDep = Annotated[LearningService, Depends(get_learning_service)]
AdminServiceDep = Annotated[AdminService, Depends(get_admin_service)]

AuthorDep = Annotated[User, Depends(require_author)]
AdminDep = Annotated[User, Depends(require_admin)]
