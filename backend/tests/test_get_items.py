from flask import json
from datetime import datetime
from tests.client import client

def test_get_items(client):
    response = client.get("/items")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "items" in data
    assert "total_price" in data

def test_get_items_with_filter(client):
    response = client.get("/items?category=Test Category")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "items" in data
    assert "total_price" in data
    for item in data["items"]:
        assert item["category"] == "Test Category"

def test_get_items_with_date_filter(client):
    start_date = "2022-01-01T00:00:00"
    end_date = "2022-12-31T23:59:59"
    response = client.get(f"/items?start_date={start_date}&end_date={end_date}")
    assert response.status_code == 200
    data = json.loads(response.data)
    assert "items" in data
    assert "total_price" in data
    for item in data["items"]:
        item_date = datetime.fromisoformat(item["last_updated_dt"])
        assert start_date <= item_date.isoformat() <= end_date
        