from fastapi import APIRouter, status

from app.dependencies import AuthorDep, LessonServiceDep
from app.schemas import LessonCreate, LessonRead

router = APIRouter(prefix="/courses/{course_id}/lessons", tags=["lessons"])


@router.get("", response_model=list[LessonRead])
async def list_course_lessons(
    course_id: int,
    service: LessonServiceDep,
) -> list[LessonRead]:
    lessons = await service.list_course_lessons(course_id)
    return [LessonRead.model_validate(lesson) for lesson in lessons]


@router.post("", response_model=LessonRead, status_code=status.HTTP_201_CREATED)
async def create_course_lesson(
    course_id: int,
    lesson_in: LessonCreate,
    service: LessonServiceDep,
    _current_user: AuthorDep,
) -> LessonRead:
    lesson = await service.create_course_lesson(course_id, lesson_in)
    return LessonRead.model_validate(lesson)
