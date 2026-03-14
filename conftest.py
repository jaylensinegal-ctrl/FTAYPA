from __future__ import annotations

import os
import tempfile
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

TEST_ROOT = Path(tempfile.mkdtemp(prefix="flighttime-pytest-"))
os.environ["DATABASE_URL"] = f"sqlite+pysqlite:///{(TEST_ROOT / 'flighttime_test.db').as_posix()}"
os.environ["UPLOADS_DIR"] = str(TEST_ROOT / "uploads")

from app.auth import DEMO_PASSWORD, ensure_demo_users
from app.database import Base, SessionLocal, engine
from app.main import app


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with SessionLocal() as db:
        ensure_demo_users(db)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth_headers(client):
    def _auth_headers(email: str = "coach@flighttime.test", password: str = DEMO_PASSWORD) -> dict[str, str]:
        response = client.post(
            "/auth/login",
            json={"email": email, "password": password},
        )
        assert response.status_code == 200, response.text
        token = response.json()["token"]
        return {"Authorization": f"Bearer {token}"}

    return _auth_headers
