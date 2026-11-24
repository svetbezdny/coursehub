import pytest
from fastapi.testclient import TestClient

from app.data import DEFAULT_COURSES, DEFAULT_LESSONS
from app.services import MIN_SEARCH_QUERY_LENGTH


def test_list_courses_returns_seed_courses(client: TestClient) -> None:
    response = client.get("/courses")

    assert response.status_code == 200, response.text

    courses = response.json()
    for dc in DEFAULT_COURSES:
        assert dc in courses


@pytest.mark.parametrize("level", ("beginner", "intermediate"))
def test_list_courses_filters_by_level(client: TestClient, level: str) -> None:
    response = client.get("/courses", params={"level": level})

    assert response.status_code == 200, response.text
    assert response.json()[0]["level"] == level


def test_list_courses_rejects_too_short_query(client: TestClient) -> None:
    response = client.get("/courses", params={"q": "q"})

    assert response.status_code == 400, response.text
    assert response.json() == {
        "detail": f"Search query must contain at least {MIN_SEARCH_QUERY_LENGTH} characters"
    }


def test_get_unknown_course_returns_404(client: TestClient) -> None:
    response = client.get("/courses/999")

    assert response.status_code == 404, response.text
    assert response.json() == {"detail": "Course not found"}


def test_get_course_with_text_id_returns_422(client: TestClient) -> None:
    response = client.get("/courses/python")

    assert response.status_code == 422, response.text
    assert response.json()["detail"][0]["loc"] == ["path", "course_id"]


def test_list_course_lessons_returns_lessons(client: TestClient) -> None:
    response = client.get("/courses/1/lessons")

    assert response.status_code == 200, response.text
    assert response.json()[0]["title"] == DEFAULT_LESSONS[0]["title"]


def test_create_lesson_persists_for_next_request(
    client: TestClient,
    author_headers: dict[str, str],
) -> None:
    course_id = 1

    response = client.post(
        f"/courses/{course_id}/lessons",
        json={"title": "Тестовый урок"},
        headers=author_headers,
    )

    assert response.status_code == 201, response.text
    created = response.json()

    list_response = client.get(f"/courses/{course_id}/lessons")
    assert list_response.status_code == 200, response.text
    assert created in list_response.json()
