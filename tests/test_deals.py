from fastapi.testclient import TestClient


def create_customer(client: TestClient) -> dict[str, object]:
    response = client.post("/customers", json={"name": "Ada Lovelace"})

    assert response.status_code == 201
    return response.json()


def create_deal(
    client: TestClient,
    customer_id: int,
    title: str = "Website redesign",
    value: str = "1500.50",
    stage: str = "lead",
    source: str = "referral",
    expected_close_date: str = "2026-07-15",
) -> dict[str, object]:
    response = client.post(
        "/deals",
        json={
            "customer_id": customer_id,
            "title": title,
            "value": value,
            "stage": stage,
            "source": source,
            "notes": "Initial discovery call booked",
            "expected_close_date": expected_close_date,
        },
    )

    assert response.status_code == 201
    return response.json()


def test_create_deal(client: TestClient) -> None:
    customer = create_customer(client)

    data = create_deal(client, customer_id=customer["id"])

    assert data["id"] == 1
    assert data["customer_id"] == customer["id"]
    assert data["title"] == "Website redesign"
    assert data["value"] == "1500.50"
    assert data["stage"] == "lead"
    assert data["source"] == "referral"
    assert data["notes"] == "Initial discovery call booked"
    assert data["expected_close_date"] == "2026-07-15"
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_create_deal_with_missing_customer_returns_404(client: TestClient) -> None:
    response = client.post(
        "/deals",
        json={
            "customer_id": 999,
            "title": "Missing customer deal",
            "value": "100.00",
            "stage": "lead",
        },
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Customer not found"}


def test_invalid_stage_returns_422(client: TestClient) -> None:
    customer = create_customer(client)

    response = client.post(
        "/deals",
        json={
            "customer_id": customer["id"],
            "title": "Invalid stage deal",
            "value": "100.00",
            "stage": "archived",
        },
    )

    assert response.status_code == 422


def test_invalid_value_returns_422(client: TestClient) -> None:
    customer = create_customer(client)

    response = client.post(
        "/deals",
        json={
            "customer_id": customer["id"],
            "title": "Invalid value deal",
            "value": "-1.00",
            "stage": "lead",
        },
    )

    assert response.status_code == 422


def test_list_deals(client: TestClient) -> None:
    customer = create_customer(client)
    first_deal = create_deal(client, customer_id=customer["id"])
    second_deal = create_deal(
        client,
        customer_id=customer["id"],
        title="Support package",
    )

    response = client.get("/deals")

    assert response.status_code == 200
    assert response.json() == [second_deal, first_deal]


def test_list_deals_limit_and_offset(client: TestClient) -> None:
    customer = create_customer(client)
    create_deal(client, customer_id=customer["id"], title="First")
    expected_deal = create_deal(client, customer_id=customer["id"], title="Second")
    create_deal(client, customer_id=customer["id"], title="Third")

    response = client.get("/deals?limit=1&offset=1")

    assert response.status_code == 200
    assert response.json() == [expected_deal]


def test_list_deals_filter_by_stage(client: TestClient) -> None:
    customer = create_customer(client)
    expected_deal = create_deal(
        client,
        customer_id=customer["id"],
        title="Proposal deal",
        stage="proposal",
    )
    create_deal(client, customer_id=customer["id"], title="Lead deal", stage="lead")

    response = client.get("/deals?stage=proposal")

    assert response.status_code == 200
    assert response.json() == [expected_deal]


def test_list_deals_filter_by_customer_id(client: TestClient) -> None:
    first_customer = create_customer(client)
    second_customer = create_customer(client)
    create_deal(client, customer_id=first_customer["id"], title="First customer deal")
    expected_deal = create_deal(
        client,
        customer_id=second_customer["id"],
        title="Second customer deal",
    )

    response = client.get(f"/deals?customer_id={second_customer['id']}")

    assert response.status_code == 200
    assert response.json() == [expected_deal]


def test_list_deals_filter_by_source(client: TestClient) -> None:
    customer = create_customer(client)
    expected_deal = create_deal(
        client,
        customer_id=customer["id"],
        title="Website deal",
        source="website",
    )
    create_deal(client, customer_id=customer["id"], title="Referral deal")

    response = client.get("/deals?source=website")

    assert response.status_code == 200
    assert response.json() == [expected_deal]


def test_list_deals_filter_by_min_value(client: TestClient) -> None:
    customer = create_customer(client)
    expected_deal = create_deal(
        client,
        customer_id=customer["id"],
        title="Large deal",
        value="2500.00",
    )
    create_deal(client, customer_id=customer["id"], title="Small deal", value="500.00")

    response = client.get("/deals?min_value=1000")

    assert response.status_code == 200
    assert response.json() == [expected_deal]


def test_list_deals_filter_by_max_value(client: TestClient) -> None:
    customer = create_customer(client)
    create_deal(client, customer_id=customer["id"], title="Large deal", value="2500.00")
    expected_deal = create_deal(
        client,
        customer_id=customer["id"],
        title="Small deal",
        value="500.00",
    )

    response = client.get("/deals?max_value=1000")

    assert response.status_code == 200
    assert response.json() == [expected_deal]


def test_list_deals_default_sorting_created_at_desc(client: TestClient) -> None:
    customer = create_customer(client)
    first_deal = create_deal(client, customer_id=customer["id"], title="First")
    second_deal = create_deal(client, customer_id=customer["id"], title="Second")
    third_deal = create_deal(client, customer_id=customer["id"], title="Third")

    response = client.get("/deals")

    assert response.status_code == 200
    assert response.json() == [third_deal, second_deal, first_deal]


def test_list_deals_ascending_sorting(client: TestClient) -> None:
    customer = create_customer(client)
    second_deal = create_deal(client, customer_id=customer["id"], title="Bravo")
    first_deal = create_deal(client, customer_id=customer["id"], title="Alpha")

    response = client.get("/deals?sort_by=title&sort_order=asc")

    assert response.status_code == 200
    assert response.json() == [first_deal, second_deal]


def test_list_deals_invalid_stage_returns_422(client: TestClient) -> None:
    response = client.get("/deals?stage=archived")

    assert response.status_code == 422


def test_list_deals_invalid_sort_by_returns_422(client: TestClient) -> None:
    response = client.get("/deals?sort_by=id")

    assert response.status_code == 422


def test_list_deals_invalid_sort_order_returns_422(client: TestClient) -> None:
    response = client.get("/deals?sort_order=random")

    assert response.status_code == 422


def test_list_deals_negative_min_value_returns_422(client: TestClient) -> None:
    response = client.get("/deals?min_value=-1")

    assert response.status_code == 422


def test_list_deals_negative_max_value_returns_422(client: TestClient) -> None:
    response = client.get("/deals?max_value=-1")

    assert response.status_code == 422


def test_get_deal_by_id(client: TestClient) -> None:
    customer = create_customer(client)
    created_deal = create_deal(client, customer_id=customer["id"])

    response = client.get(f"/deals/{created_deal['id']}")

    assert response.status_code == 200
    assert response.json() == created_deal


def test_missing_deal_returns_404(client: TestClient) -> None:
    response = client.get("/deals/999")

    assert response.status_code == 404
    assert response.json() == {"detail": "Deal not found"}


def test_partial_update_preserves_omitted_fields(client: TestClient) -> None:
    customer = create_customer(client)
    created_deal = create_deal(client, customer_id=customer["id"])

    response = client.patch(
        f"/deals/{created_deal['id']}",
        json={"stage": "proposal", "value": "2000.00"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["customer_id"] == created_deal["customer_id"]
    assert data["title"] == created_deal["title"]
    assert data["value"] == "2000.00"
    assert data["stage"] == "proposal"
    assert data["source"] == created_deal["source"]
    assert data["notes"] == created_deal["notes"]
    assert data["expected_close_date"] == created_deal["expected_close_date"]


def test_delete_deal(client: TestClient) -> None:
    customer = create_customer(client)
    created_deal = create_deal(client, customer_id=customer["id"])

    response = client.delete(f"/deals/{created_deal['id']}")

    assert response.status_code == 204
    assert response.content == b""


def test_deleted_deal_is_no_longer_returned(client: TestClient) -> None:
    customer = create_customer(client)
    created_deal = create_deal(client, customer_id=customer["id"])

    delete_response = client.delete(f"/deals/{created_deal['id']}")
    get_response = client.get(f"/deals/{created_deal['id']}")

    assert delete_response.status_code == 204
    assert get_response.status_code == 404
