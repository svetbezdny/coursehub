import pytest
from fastapi.testclient import TestClient

from app.schemas import AdminStatsRead


@pytest.mark.parametrize(
    "role_fixture_name",
    ["student_headers", "author_headers"],
)
def test_admin_stats_requires_admin(
    client: TestClient, role_fixture_name, request
) -> None:
    role = request.getfixturevalue(role_fixture_name)
    response = client.get("/admin/stats", headers=role)

    assert response.status_code == 403, response.text
    assert response.json() == {"detail": "Not enough permissions"}


def test_admin_stats_returns_counts(
    client: TestClient, admin_headers: dict[str, str]
) -> None:
    response = client.get("/admin/stats", headers=admin_headers)

    assert response.status_code == 200, response.text

    data = response.json()

    for field in list(AdminStatsRead.model_fields.keys()):
        assert field in data, f"Missing field {field} in response"

    assert data["courses"] >= 1
    assert data["users"] >= 1
