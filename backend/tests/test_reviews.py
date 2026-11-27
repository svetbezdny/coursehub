import pytest
from fastapi.testclient import TestClient


def test_student_can_review_enrolled_course(
    client: TestClient, student_headers: dict[str, str]
) -> None:
    client.post("/courses/1/enroll", headers=student_headers)

    response = client.post(
        "/courses/1/reviews",
        headers=student_headers,
        json={"rating": 5, "comment": "Отличный старт для FastAPI"},
    )

    assert response.status_code == 201, response.text
    assert response.json() == {
        "id": 1,
        "course_id": 1,
        "user_id": 3,
        "rating": 5,
        "comment": "Отличный старт для FastAPI",
    }


def test_review_requires_enrollment(
    client: TestClient, student_headers: dict[str, str]
) -> None:
    response = client.post(
        "/courses/1/reviews",
        headers=student_headers,
        json={"rating": 4, "comment": "Not bad"},
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Enroll in course before leaving a review"}


def test_review_rejects_second_review_for_same_course(
    client: TestClient,
    student_headers: dict[str, str],
) -> None:
    client.post("/courses/1/enroll", headers=student_headers)
    client.post(
        "/courses/1/reviews",
        headers=student_headers,
        json={"rating": 5, "comment": "Первый отзыв"},
    )

    response = client.post(
        "/courses/1/reviews",
        headers=student_headers,
        json={"rating": 4, "comment": "Второй отзыв"},
    )

    assert response.status_code == 400, response.text
    assert response.json() == {"detail": "Review already exists for this course"}


@pytest.mark.parametrize("rating", (0, 6))
def test_review_rejects_invalid_rating(
    client: TestClient, student_headers: dict[str, str], rating: int
) -> None:
    client.post("/courses/1/enroll", headers=student_headers)

    response = client.post(
        "/courses/1/reviews",
        headers=student_headers,
        json={"rating": rating, "comment": "Не корректная оценка"},
    )

    assert response.status_code == 422, response.text
    assert response.json()["detail"][0]["loc"] == ["body", "rating"]


def test_list_course_reviews(
    client: TestClient, student_headers: dict[str, str]
) -> None:
    client.post("/courses/1/enroll", headers=student_headers)
    client.post(
        "/courses/1/reviews",
        headers=student_headers,
        json={"rating": 5, "comment": "Отличный старт для FastAPI"},
    )

    response = client.get("/courses/1/reviews")

    assert response.status_code == 200, response.text
    assert response.json() == [
        {
            "id": 1,
            "course_id": 1,
            "user_id": 3,
            "rating": 5,
            "comment": "Отличный старт для FastAPI",
        }
    ]
