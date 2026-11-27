from fastapi import APIRouter, status

from app.dependencies import CurrentUserDep, ReviewServiceDep
from app.schemas import ReviewCreate, ReviewRead

router = APIRouter(prefix="/courses/{course_id}/reviews", tags=["reviews"])


@router.get("", response_model=list[ReviewRead])
async def list_course_reviews(
    course_id: int,
    service: ReviewServiceDep,
) -> list[ReviewRead]:
    return await service.list_course_reviews(course_id)


@router.post("", response_model=ReviewRead, status_code=status.HTTP_201_CREATED)
async def create_course_review(
    course_id: int,
    review_in: ReviewCreate,
    current_user: CurrentUserDep,
    service: ReviewServiceDep,
) -> ReviewRead:
    return await service.create_review(
        course_id=course_id, user=current_user, review_in=review_in
    )
