import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import DATABASE_URL
from pathlib import Path

client = TestClient(app)

def setup_module(module):
    # Ensure a clean DB file before running tests
    db_file = Path("todo.db")
    if db_file.exists():
        db_file.unlink()

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"

def test_crud_flow():
    # Create
    r = client.post("/todos", json={"title": "Buy milk"})
    assert r.status_code == 201
    todo = r.json()
    todo_id = todo["id"]
    assert todo["title"] == "Buy milk"
    assert todo["done"] is False

    # List
    r = client.get("/todos?page=1&page_size=5")
    assert r.status_code == 200
    data = r.json()
    assert any(i["id"] == todo_id for i in data["items"])

    # Update
    r = client.patch(f"/todos/{todo_id}", json={"done": True})
    assert r.status_code == 200
    assert r.json()["done"] is True

    # Filter
    r = client.get("/todos?done=true")
    assert r.status_code == 200
    assert any(i["id"] == todo_id for i in r.json()["items"])

    # Delete
    r = client.delete(f"/todos/{todo_id}")
    assert r.status_code == 204

    # Not found after delete (update attempt)
    r = client.patch(f"/todos/{todo_id}", json={"done": False})
    assert r.status_code == 404
