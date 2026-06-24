from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database.database import Base, get_db
from app.main import app

engine = create_engine(
    "sqlite+pysqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    Base.metadata.create_all(bind=engine)

    def override_get_db() -> Generator[Session, None, None]:
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


def create_customer(
    client: TestClient,
    name: str = "Ada Lovelace",
) -> dict[str, object]:
    response = client.post(
        "/customers",
        json={
            "name": name,
            "email": "ada@example.com",
            "phone": "+1 555 0101",
            "company": "Analytical Engines",
            "notes": "First customer",
        },
    )

    assert response.status_code == 201
    return response.json()


def test_create_customer(client: TestClient) -> None:
    data = create_customer(client)

    assert data["id"] == 1
    assert data["name"] == "Ada Lovelace"
    assert data["email"] == "ada@example.com"
    assert data["phone"] == "+1 555 0101"
    assert data["company"] == "Analytical Engines"
    assert data["notes"] == "First customer"
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_list_customers(client: TestClient) -> None:
    first_customer = create_customer(client, name="Ada Lovelace")
    second_customer = create_customer(client, name="Grace Hopper")

    response = client.get("/customers")

    assert response.status_code == 200
    assert response.json() == [first_customer, second_customer]


def test_get_customer_by_id(client: TestClient) -> None:
    created_customer = create_customer(client)

    response = client.get(f"/customers/{created_customer['id']}")

    assert response.status_code == 200
    assert response.json() == created_customer


def test_missing_customer_returns_404(client: TestClient) -> None:
    response = client.get("/customers/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Customer not found"}


def test_partial_update_preserves_omitted_fields(client: TestClient) -> None:
    created_customer = create_customer(client)

    response = client.patch(
        f"/customers/{created_customer['id']}",
        json={"company": "Updated Company"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == created_customer["name"]
    assert data["email"] == created_customer["email"]
    assert data["phone"] == created_customer["phone"]
    assert data["company"] == "Updated Company"
    assert data["notes"] == created_customer["notes"]


def test_delete_customer(client: TestClient) -> None:
    created_customer = create_customer(client)

    response = client.delete(f"/customers/{created_customer['id']}")

    assert response.status_code == 204
    assert response.content == b""


def test_deleted_customer_is_no_longer_returned(client: TestClient) -> None:
    created_customer = create_customer(client)

    delete_response = client.delete(f"/customers/{created_customer['id']}")
    get_response = client.get(f"/customers/{created_customer['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404


def test_customer_can_be_created_without_optional_fields(client: TestClient) -> None:
    response = client.post("/customers", json={"name": "No Email"})

    assert response.status_code == 201
    data = response.json()
    assert data["email"] is None
    assert data["phone"] is None
    assert data["company"] is None
    assert data["notes"] is None
