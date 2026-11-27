from decimal import Decimal
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints

CourseLevel = Literal["beginner", "intermediate", "advanced"]
UserRole = Literal["student", "author", "admin"]

CourseTitle = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=3, max_length=80)
]
LessonTitle = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=3, max_length=120)
]


class CourseRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    slug: str
    level: CourseLevel
    price: float


class CourseCreate(BaseModel):
    title: CourseTitle
    level: CourseLevel
    price: Decimal = Field(
        default=Decimal("0.00"), ge=0, max_digits=10, decimal_places=2
    )


class CourseUpdate(BaseModel):
    title: CourseTitle | None = None
    level: CourseLevel | None = None
    price: Decimal | None = Field(default=None, ge=0, max_digits=10, decimal_places=2)


class LessonRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    course_id: int
    title: str
    order: int


class LessonCreate(BaseModel):
    title: LessonTitle
    order: int | None = Field(default=None, ge=1)


class UserRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: EmailStr
    full_name: str | None
    role: UserRole


class UserCreate(BaseModel):
    email: EmailStr = Field(min_length=5, max_length=120)
    password: str = Field(min_length=8, max_length=128)
    full_name: str | None = Field(default=None, max_length=120)


class UserLogin(BaseModel):
    email: EmailStr = Field(min_length=5, max_length=120)
    password: str = Field(min_length=1, max_length=128)


class TokenRead(BaseModel):
    access_token: str
    token_type: str = "bearer"


class EnrollmentRead(BaseModel):
    id: int
    user_id: int
    course_id: int
    course_title: str


class LessonProgressRead(BaseModel):
    lesson_id: int
    course_id: int
    completed: bool


class CourseProgressRead(BaseModel):
    course_id: int
    course_title: str
    completed_lessons: int
    completed_lesson_ids: list[int]
    total_lessons: int
    percent: float


class FavoriteRead(BaseModel):
    id: int
    user_id: int
    course_id: int
    course_title: str


class AdminStatsRead(BaseModel):
    courses: int
    lessons: int
    users: int
    enrollments: int
    completed_lessons: int
    favorite_courses: int
    reviews: int


class ReviewCreate(BaseModel):
    rating: int = Field(ge=1, le=5)
    comment: str | None = Field(default=None, max_length=500)


class ReviewRead(BaseModel):
    id: int
    course_id: int
    user_id: int
    rating: int
    comment: str | None
