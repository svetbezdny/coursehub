from fastapi.testclient import TestClient

from app.config import settings


def test_health_returns_service_status(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200, response.text
    assert response.json() == {
        "status": "ok",
        "service": settings.app_title,
    }


def test_ready_returns_service_and_database_status(client: TestClient) -> None:
    response = client.get("/ready")

    assert response.status_code == 200, response.text
    assert response.json() == {
        "status": "ready",
        "service": settings.app_title,
        "database": "ok",
    }


def test_version_returns_app_metadata(client: TestClient) -> None:
    response = client.get("/version")

    assert response.status_code == 200, response.text
    assert response.json() == {
        "name": settings.app_title,
        "version": settings.app_version,
        "environment": settings.environment,
    }


def test_request_id_header_is_returned(client: TestClient) -> None:
    response = client.get("/health", headers={"X-Request-ID": "123456789"})

    assert response.status_code == 200, response.text
    assert response.headers["X-Request-ID"] == "123456789"


def test_request_id_header_is_generated(client: TestClient) -> None:
    response = client.get("/health")

    assert response.status_code == 200, response.text
    assert response.headers["X-Request-ID"]
