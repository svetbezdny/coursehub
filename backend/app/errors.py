class CourseHubError(Exception):
    status_code = 400
    detail = "CourseHub error"

    def __init__(self, detail: str | None = None) -> None:
        if detail is not None:
            self.detail = detail
        super().__init__(self.detail)


class CourseNotFoundError(CourseHubError):
    status_code = 404
    detail = "Course not found"


class SearchQueryTooShortError(CourseHubError):
    def __init__(self, min_length: int) -> None:
        super().__init__(f"Search query must contain at least {min_length} characters")


class EmailAlreadyRegisteredError(CourseHubError):
    detail = "Email already registered"


class InvalidCredentialsError(CourseHubError):
    status_code = 401
    detail = "Invalid email or password"


class InvalidTokenError(CourseHubError):
    status_code = 401
    detail = "Invalid or expired token"


class PermissionDeniedError(CourseHubError):
    status_code = 403
    detail = "Not enough permissions"


class EnrollmentAlreadyExistsError(CourseHubError):
    detail = "User is already enrolled in this course"


class LessonNotFoundError(CourseHubError):
    status_code = 404
    detail = "Lesson not found"


class EnrollmentRequiredError(CourseHubError):
    detail = "Enroll in course before completing lessons"


class FavoriteAlreadyExistsError(CourseHubError):
    detail = "Course is already in favorites"


class ReviewEnrollmentRequiredError(CourseHubError):
    detail = "Enroll in course before leaving a review"


class ReviewAlreadyExistsError(CourseHubError):
    detail = "Review already exists for this course"
