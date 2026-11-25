from fastapi.testclient import TestClient

from app.data import DEFAULT_COURSES


def test_student_can_enroll_in_course(
    client: TestClient, student_headers: dict[str, str]
) -> None:
    response = client.post("/courses/1/enroll", headers=student_headers)

    assert response.status_code == 201, response.text
    assert response.json() == {
        "id": 1,
        "user_id": 3,
        "course_id": 1,
        "course_title": DEFAULT_COURSES[0]["title"],
    }


def test_student_can_complete_lesson_after_enrollment(
    client: TestClient,
    student_headers: dict[str, str],
) -> None:
    response1 = client.post("/courses/1/enroll", headers=student_headers)

    assert response1.status_code == 201, response1.text

    response = client.post("/lessons/1/complete", headers=student_headers)

    assert response.status_code == 200, response.text
    assert response.json() == {
        "lesson_id": 1,
        "course_id": 1,
        "completed": True,
    }


def test_learning_endpoints_require_token(client: TestClient) -> None:
    response = client.get("/me/enrollments")

    assert response.status_code == 401, response.text
    assert response.json() == {"detail": "Invalid or expired token"}
