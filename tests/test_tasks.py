from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_list_tasks():
    r = client.get("/tasks")
    assert r.status_code == 200
    assert isinstance(r.json(), list)

def test_create_task():
    r = client.post("/tasks", json={"title": "test task", "done": False})
    assert r.status_code == 201
    data = r.json()
    assert "id" in data
    assert data["title"] == "test task"
    assert data["done"] is False

def test_patch_done_only():
    created = client.post("/tasks", json={"title": "patch me", "done": False}).json()
    task_id = created["id"]

    r = client.patch(f"/tasks/{task_id}", json={"done": True})
    assert r.status_code == 200
    data = r.json()
    assert data["done"] is True

def test_delete_task():
    created = client.post("/tasks", json={"title": "delete me", "done": False}).json()
    task_id = created["id"]

    r = client.delete(f"/tasks/{task_id}")
    assert r.status_code == 204

def test_delete_missing_returns_404():
    r = client.delete("/tasks/999999")
    assert r.status_code == 404
