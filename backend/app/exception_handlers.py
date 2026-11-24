from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.errors import CourseHubError, InvalidCredentialsError, InvalidTokenError


async def coursehub_error_handler(request: Request, error: Exception) -> JSONResponse:
    assert isinstance(error, CourseHubError)

    headers = {}
    if isinstance(error, InvalidCredentialsError | InvalidTokenError):
        headers["WWW-Authenticate"] = "Bearer"

    return JSONResponse(
        status_code=error.status_code,
        content={"detail": error.detail},
        headers=headers,
    )


def register_exception_handlers(app: FastAPI) -> None:
    app.add_exception_handler(CourseHubError, coursehub_error_handler)
