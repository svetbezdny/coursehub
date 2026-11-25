from collections.abc import AsyncGenerator, Generator
from contextlib import asynccontextmanager

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import StaticPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from app.database import get_session, seed_database
from app.main import create_app
from app.models import Base, User
from app.security import hash_password

AUTHOR_EMAIL = "test_author@test.com"
AUTHOR_PASSWORD = "test_author_password"
STUDENT_EMAIL = "test_student@test.com"
STUDENT_PASSWORD = "test_student_password"
ADMIN_EMAIL = "test_admin@test.com"
ADMIN_PASSWORD = "test_admin_password"


@pytest.fixture
def client() -> Generator[TestClient]:
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    testing_session_maker = async_sessionmaker(engine, expire_on_commit=False)

    @asynccontextmanager
    async def test_lifespan(_: FastAPI) -> AsyncGenerator[None]:
        try:
            async with engine.begin() as connection:
                await connection.run_sync(Base.metadata.create_all)

            await seed_database(testing_session_maker)
            async with testing_session_maker() as session:
                session.add_all(
                    [
                        User(
                            email=ADMIN_EMAIL,
                            role="admin",
                            hashed_password=hash_password(ADMIN_PASSWORD),
                        ),
                        User(
                            email=AUTHOR_EMAIL,
                            role="author",
                            hashed_password=hash_password(AUTHOR_PASSWORD),
                        ),
                        User(
                            email=STUDENT_EMAIL,
                            role="student",
                            hashed_password=hash_password(STUDENT_PASSWORD),
                        ),
                    ]
                )
                await session.commit()
            yield
        finally:
            await engine.dispose()

    async def override_get_session():
        async with testing_session_maker() as session:
            yield session

    test_app = create_app(lifespan_handler=test_lifespan)
    test_app.dependency_overrides[get_session] = override_get_session

    with TestClient(test_app) as test_client:
        yield test_client


@pytest.fixture
def author_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/auth/login",
        json={"email": AUTHOR_EMAIL, "password": AUTHOR_PASSWORD},
    )

    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def student_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/auth/login",
        json={"email": STUDENT_EMAIL, "password": STUDENT_PASSWORD},
    )

    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def admin_headers(client: TestClient) -> dict[str, str]:
    response = client.post(
        "/auth/login",
        json={"email": ADMIN_EMAIL, "password": ADMIN_PASSWORD},
    )

    assert response.status_code == 200, response.text
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
