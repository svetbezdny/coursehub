from fastapi import APIRouter, status

from app.dependencies import CurrentUserDep, LearningServiceDep
from app.schemas import (
    CourseProgressRead,
    EnrollmentRead,
    FavoriteRead,
    LessonProgressRead,
)

router = APIRouter(tags=["learning"])


@router.get("/me/enrollments", response_model=list[EnrollmentRead])
async def list_my_enrollments(
    current_user: CurrentUserDep,
    service: LearningServiceDep,
) -> list[EnrollmentRead]:
    return await service.list_my_enrollments(current_user)


@router.post(
    "/courses/{course_id}/enroll",
    response_model=EnrollmentRead,
    status_code=status.HTTP_201_CREATED,
)
async def enroll_in_course(
    course_id: int,
    current_user: CurrentUserDep,
    service: LearningServiceDep,
) -> EnrollmentRead:
    return await service.enroll(course_id=course_id, user=current_user)


@router.post(
    "/lessons/{lesson_id}/complete",
    response_model=LessonProgressRead,
)
async def complete_lesson(
    lesson_id: int,
    current_user: CurrentUserDep,
    service: LearningServiceDep,
) -> LessonProgressRead:
    return await service.complete_lesson(lesson_id=lesson_id, user=current_user)


@router.get(
    "/me/progress",
    response_model=list[CourseProgressRead],
)
async def list_my_progress(
    current_user: CurrentUserDep,
    service: LearningServiceDep,
) -> list[CourseProgressRead]:
    return await service.list_my_progress(current_user)


@router.post(
    "/courses/{course_id}/favorite",
    response_model=FavoriteRead,
    status_code=status.HTTP_201_CREATED,
)
async def favorite_course(
    course_id: int,
    current_user: CurrentUserDep,
    service: LearningServiceDep,
) -> FavoriteRead:
    return await service.favorite_course(course_id=course_id, user=current_user)


@router.get("/me/favorites", response_model=list[FavoriteRead])
async def list_my_favorites(
    current_user: CurrentUserDep,
    service: LearningServiceDep,
) -> list[FavoriteRead]:
    return await service.list_my_favorites(current_user)


@router.delete(
    "/courses/{course_id}/favorite",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def remove_favorite_course(
    course_id: int,
    current_user: CurrentUserDep,
    service: LearningServiceDep,
) -> None:
    await service.remove_favorite_course(course_id=course_id, user=current_user)
