from typing import Any

import pytest
from fastapi.testclient import TestClient

from app.security import create_access_token, decode_access_token
from tests.conftest import (
    AUTHOR_EMAIL,
    AUTHOR_PASSWORD,
)


def test_register_user_returns_user_without_password(client: TestClient):
    email = "new-student@example.com"

    response = client.post(
        "/auth/register",
        json={
            "email": email,
            "password": "student-pass-123",
            "full_name": "New Student",
        },
    )

    assert response.status_code == 201, response.text

    body = response.json()
    assert body["email"] == email
    assert body["role"] == "student"
    assert "student-pass-123" not in response.text
    assert "hashed_password" not in response.text


def test_login_returns_bearer_token(client: TestClient):
    response = client.post(
        "/auth/login",
        json={"email": AUTHOR_EMAIL, "password": AUTHOR_PASSWORD},
    )

    assert response.status_code == 200, response.text

    body = response.json()
    assert body["token_type"] == "bearer"
    assert body["access_token"].count(".") == 2


def test_login_rejects_wrong_password(client: TestClient) -> None:
    response = client.post(
        "/auth/login",
        json={"email": AUTHOR_EMAIL, "password": "wrong-password"},
    )

    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Invalid email or password"}


def test_users_me_returns_current_user(
    client: TestClient, author_headers: dict[str, str]
) -> None:
    response = client.get("/users/me", headers=author_headers)

    assert response.status_code == 200, response.text
    assert response.json()["email"] == AUTHOR_EMAIL


def test_create_course_rejects_student_role(
    client: TestClient, student_headers: dict[str, str]
) -> None:
    response = client.post(
        "/courses",
        headers=student_headers,
        json={
            "title": "Student Course",
            "slug": "student-course",
            "level": "beginner",
            "price": 0,
        },
    )

    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Not enough permissions"}


def test_update_course_requires_author_role(
    client: TestClient,
    student_headers: dict[str, str],
) -> None:
    response = client.patch(
        "/courses/1",
        headers=student_headers,
        json={"title": "Student Update"},
    )

    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Not enough permissions"}


def test_create_course_lesson_requires_author_role(
    client: TestClient,
    student_headers: dict[str, str],
) -> None:
    response = client.post(
        "/courses/1/lessons",
        headers=student_headers,
        json={"title": "Student Lesson"},
    )

    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Not enough permissions"}


@pytest.mark.parametrize(
    ("url", "method", "json"),
    (
        [
            (
                "/courses",
                "post",
                {
                    "title": "No Token Course",
                    "slug": "no-token-course",
                    "level": "beginner",
                    "price": 0,
                },
            ),
            ("/courses/1", "patch", {"title": "Missing Token"}),
            ("/courses/1/lessons", "post", {"title": "Missing Token"}),
        ]
    ),
)
def test_courses_requires_token(
    client: TestClient, url: str, method: str, json: dict[str, Any]
) -> None:
    client_method = getattr(client, method)
    response = client_method(
        url,
        json=json,
    )

    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Invalid or expired token"}


def test_access_token_is_expired_at_exp_time(monkeypatch) -> None:
    secret_key = "test-secret-for-hs256-at-least-32-bytes"

    monkeypatch.setattr("app.security.time.time", lambda: 1_000_000)
    token = create_access_token(
        subject="1",
        secret_key=secret_key,
        expires_in_seconds=30,
    )
    monkeypatch.setattr("app.security.time.time", lambda: 1_000_030)

    assert decode_access_token(token, secret_key=secret_key) is None
