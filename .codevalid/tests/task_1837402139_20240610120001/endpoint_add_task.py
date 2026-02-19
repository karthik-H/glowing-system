import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Helper to generate max length strings
def repeat(char, times):
    return char * times

@pytest.mark.parametrize("payload,expected_status,expected_body", [
    # Test Case 1: Create Task with All Required Fields
    (
        {
            "description": "This is a sample task description.",
            "due_date": "2024-07-10",
            "priority": 2,
            "title": "Sample Task",
            "user_name": "johndoe"
        },
        201,
        {
            "description": "This is a sample task description.",
            "due_date": "2024-07-10",
            "priority": 2,
            "title": "Sample Task",
            "user_name": "johndoe"
            # 'id' will be checked separately
        }
    ),
])
def test_create_task_with_all_required_fields(payload, expected_status, expected_body):
    response = client.post("/tasks", json=payload)
    assert response.status_code == expected_status
    data = response.json()
    for k, v in expected_body.items():
        assert data[k] == v
    assert isinstance(data["id"], int)

def test_create_task_missing_title():
    payload = {
        "description": "Missing title.",
        "due_date": "2024-07-10",
        "priority": 1,
        "user_name": "johndoe"
    }
    response = client.post("/tasks", json=payload)
    # FastAPI/Pydantic returns 422 for missing required fields
    assert response.status_code == 422 or response.status_code == 400
    if response.status_code == 422:
        assert "title" in response.text
    else:
        assert response.json()["error"] == "'title' field is required."

def test_create_task_missing_description():
    payload = {
        "due_date": "2024-07-10",
        "priority": 2,
        "title": "Task without description",
        "user_name": "janedoe"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422 or response.status_code == 400
    if response.status_code == 422:
        assert "description" in response.text
    else:
        assert response.json()["error"] == "'description' field is required."

def test_create_task_missing_priority():
    payload = {
        "description": "Priority missing.",
        "due_date": "2024-07-10",
        "title": "Task without priority",
        "user_name": "janedoe"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422 or response.status_code == 400
    if response.status_code == 422:
        assert "priority" in response.text
    else:
        assert response.json()["error"] == "'priority' field is required."

def test_create_task_missing_due_date():
    payload = {
        "description": "Due date missing.",
        "priority": 2,
        "title": "Task without due_date",
        "user_name": "janedoe"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422 or response.status_code == 400
    if response.status_code == 422:
        assert "due_date" in response.text
    else:
        assert response.json()["error"] == "'due_date' field is required."

def test_create_task_missing_user_name():
    payload = {
        "description": "User name missing.",
        "due_date": "2024-07-10",
        "priority": 2,
        "title": "Task without user_name"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422 or response.status_code == 400
    if response.status_code == 422:
        assert "user_name" in response.text
    else:
        assert response.json()["error"] == "'user_name' field is required."

def test_create_task_with_extra_location_field():
    payload = {
        "description": "Location field included.",
        "due_date": "2024-07-10",
        "location": "New York",
        "priority": 1,
        "title": "Task with location",
        "user_name": "johndoe"
    }
    response = client.post("/tasks", json=payload)
    # FastAPI/Pydantic returns 422 for extra fields unless allow_extra is set
    assert response.status_code == 422 or response.status_code == 400
    if response.status_code == 422:
        assert "location" in response.text
    else:
        assert response.json()["error"] == "'location' field is not accepted."

def test_create_task_with_minimum_length_fields():
    payload = {
        "description": "B",
        "due_date": "2024-07-10",
        "priority": 1,
        "title": "A",
        "user_name": "C"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == "B"
    assert data["due_date"] == "2024-07-10"
    assert data["priority"] == 1
    assert data["title"] == "A"
    assert data["user_name"] == "C"
    assert isinstance(data["id"], int)

def test_create_task_with_maximum_length_fields():
    payload = {
        "description": repeat("D", 1000),
        "due_date": "2024-07-10",
        "priority": 5,
        "title": repeat("T", 100),
        "user_name": repeat("U", 50)
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["description"] == repeat("D", 1000)
    assert data["due_date"] == "2024-07-10"
    assert data["priority"] == 5
    assert data["title"] == repeat("T", 100)
    assert data["user_name"] == repeat("U", 50)
    assert isinstance(data["id"], int)

def test_create_task_with_invalid_priority_type():
    payload = {
        "description": "Priority should be int.",
        "due_date": "2024-07-10",
        "priority": "high",
        "title": "Task with invalid priority",
        "user_name": "janedoe"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422 or response.status_code == 400
    if response.status_code == 422:
        assert "priority" in response.text
    else:
        assert response.json()["error"] == "'priority' must be an integer."

def test_create_task_with_invalid_due_date_format():
    payload = {
        "description": "Due date in wrong format.",
        "due_date": "10-07-2024",
        "priority": 2,
        "title": "Task with invalid due_date",
        "user_name": "janedoe"
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422 or response.status_code == 400
    if response.status_code == 422:
        assert "due_date" in response.text
    else:
        assert response.json()["error"] == "'due_date' must be in YYYY-MM-DD format."

def test_create_task_with_empty_string_fields():
    payload = {
        "description": "",
        "due_date": "2024-07-10",
        "priority": 1,
        "title": "",
        "user_name": ""
    }
    response = client.post("/tasks", json=payload)
    assert response.status_code == 422 or response.status_code == 400
    if response.status_code == 422:
        assert "ensure this value has at least 1 characters" in response.text
    else:
        assert response.json()["error"] == "Fields 'title', 'description', and 'user_name' cannot be empty."

def test_create_task_with_invalid_json_body():
    response = client.post("/tasks", data="invalid json", headers={"Content-Type": "application/json"})
    # FastAPI returns 422 for invalid JSON
    assert response.status_code == 422 or response.status_code == 400
    if response.status_code == 422:
        assert "JSON" in response.text
    else:
        assert response.json()["error"] == "Request body must be valid JSON."

def test_get_method_not_allowed_on_tasks():
    response = client.get("/tasks")
    assert response.status_code == 405
    assert response.json()["detail"] == "Method Not Allowed" or response.json().get("error") == "Method Not Allowed"