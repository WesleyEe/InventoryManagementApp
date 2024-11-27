from flask import json
from tests.client import client

def test_add_item(client):
    data = {
        "name": "Test Item 2",
        "category": "Test Category",
        "price": 10.99
    }
    response = client.post("/item", json=data)
    assert response.status_code == 201 or response.status_code == 200
    data = json.loads(response.data)
    assert data["message"] == "Item created" or data["message"] == "Item updated"
    assert "id" in data
