from tests.client import client

def test_get_filtered_items_with_name_filter(client):
    response = client.post(
        "/items-filter-page-sort", json={"filters": {"name": "Test Item"}}
    )
    assert response.status_code == 200
    data = response.json
    assert "items" in data
    for item in data["items"]:
        assert "Test Item" in item["name"]


def test_get_filtered_items_with_category_filter(client):
    response = client.post(
        "/items-filter-page-sort", json={"filters": {"category": "Test Category"}}
    )
    assert response.status_code == 200
    data = response.json
    assert "items" in data
    for item in data["items"]:
        assert item["category"] == "Test Category"


def test_get_filtered_items_with_price_range_filter(client):
    response = client.post(
        "/items-filter-page-sort", json={"filters": {"price_range": [10.0, 20.0]}}
    )
    assert response.status_code == 200
    data = response.json
    assert "items" in data

    for item in data["items"]:
        assert 10.0 <= float(item["price"]) <= 20.0


def test_get_filtered_items_with_pagination(client):
    response = client.post(
        "/items-filter-page-sort", json={"pagination": {"page": 1, "limit": 5}}
    )
    assert response.status_code == 200
    data = response.json
    assert "items" in data
    assert len(data["items"]) <= 5


def test_get_filtered_items_with_sorting(client):
    response = client.post(
        "/items-filter-page-sort",
        json={"sort": {"field": "last_updated_dt", "order": "desc"}},
    )
    assert response.status_code == 200
    data = response.json
    assert "items" in data
    items = data["items"]
    assert all(
        items[i]["last_updated_dt"] >= items[i + 1]["last_updated_dt"]
        for i in range(len(items) - 1)
    )


def test_get_filtered_items_with_multiple_filters(client):
    response = client.post(
        "/items-filter-page-sort",
        json={
            "filters": {"name": "Test Item", "category": "Test Category"},
            "pagination": {"page": 1, "limit": 5},
            "sort": {"field": "last_updated_dt", "order": "desc"},
        },
    )
    assert response.status_code == 200
    data = response.json
    assert "items" in data
    items = data["items"]
    assert all(
        "Test Item" in item["name"] and item["category"] == "Test Category"
        for item in items
    )
    assert len(items) <= 5
    assert all(
        items[i]["last_updated_dt"] >= items[i + 1]["last_updated_dt"]
        for i in range(len(items) - 1)
    )
