from fastapi import APIRouter, status

from app.dependencies import AuthorDep, CourseServiceDep
from app.schemas import CourseCreate, CourseLevel, CourseRead, CourseUpdate

router = APIRouter(prefix="/courses", tags=["courses"])


@router.get("", response_model=list[CourseRead])
async def list_courses(
    *,
    level: CourseLevel | None = None,
    q: str | None = None,
    service: CourseServiceDep,
) -> list[CourseRead]:
    courses = await service.list_courses(level=level, q=q)
    return [CourseRead.model_validate(course) for course in courses]


@router.get("/{course_id}", response_model=CourseRead)
async def get_course(
    course_id: int,
    service: CourseServiceDep,
) -> CourseRead:
    course = await service.get_course(course_id)
    return CourseRead.model_validate(course)


@router.post("", response_model=CourseRead, status_code=status.HTTP_201_CREATED)
async def create_course(
    course_in: CourseCreate,
    service: CourseServiceDep,
    _current_user: AuthorDep,
) -> CourseRead:
    course = await service.create_course(course_in)
    return CourseRead.model_validate(course)


@router.patch("/{course_id}", response_model=CourseRead)
async def update_course(
    course_id: int,
    course_in: CourseUpdate,
    service: CourseServiceDep,
    _current_user: AuthorDep,
) -> CourseRead:
    course = await service.update_course(course_id, course_in)
    return CourseRead.model_validate(course)
