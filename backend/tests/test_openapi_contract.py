from fastapi.testclient import TestClient


def test_openapi_contains_current_coursehub_paths(client: TestClient) -> None:
    response = client.get("/openapi.json")

    assert response.status_code == 200
    paths = response.json()["paths"]
    expected_paths = {
        "/health",
        "/ready",
        "/version",
        "/auth/register",
        "/auth/login",
        "/users/me",
        "/courses",
        "/courses/{course_id}",
        "/courses/{course_id}/lessons",
        "/me/enrollments",
        "/courses/{course_id}/enroll",
        "/lessons/{lesson_id}/complete",
        "/me/progress",
        "/courses/{course_id}/favorite",
        "/me/favorites",
    }
    assert expected_paths.issubset(paths)
