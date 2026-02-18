import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.domain.models.task import TaskCreate, Task
from unittest.mock import patch, MagicMock

client = TestClient(app)

# Helper to generate a Task response with auto-generated id
def make_task_response(body):
    resp = body.copy()
    resp['id'] = 'auto_generated_id'
    return resp

@pytest.fixture(autouse=True)
def clear_tasks():
    # In real tests, clear DB or mock repository here
    pass

# Test Case 1: Create task with all valid fields
def test_create_task_with_all_valid_fields():
    payload = {
        'description': 'Complete the draft and send for review',
        'due_date': '2024-07-01',
        'priority': 3,
        'tag': 'work',
        'title': 'Finish project report',
        'user_name': 'alice'
    }
    expected = make_task_response(payload)
    with patch('app.services.task_service.TaskService.create_task', return_value=Task(**expected)):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 201
    resp_json = response.json()
    assert resp_json == expected

# Test Case 2: Create task with minimal required fields
def test_create_task_with_minimal_required_fields():
    payload = {
        'description': '',
        'due_date': '2024-06-15',
        'priority': 1,
        'tag': '',
        'title': 'Buy groceries',
        'user_name': 'bob'
    }
    expected = make_task_response(payload)
    with patch('app.services.task_service.TaskService.create_task', return_value=Task(**expected)):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 201
    assert response.json() == expected

# Test Case 3: Create task with missing title
def test_create_task_with_missing_title():
    payload = {
        'description': 'No title provided',
        'due_date': '2024-06-20',
        'priority': 2,
        'tag': 'personal',
        'user_name': 'charlie'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception("'title' is a required field")):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': "'title' is a required field"}

# Test Case 4: Create task with empty string title
def test_create_task_with_empty_string_title():
    payload = {
        'description': 'Empty title test',
        'due_date': '2024-06-20',
        'priority': 2,
        'tag': 'errand',
        'title': '',
        'user_name': 'dave'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception("'title' must not be empty")):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': "'title' must not be empty"}

# Test Case 5: Create task with priority as string
def test_create_task_with_priority_as_string():
    payload = {
        'description': 'Call on Sunday',
        'due_date': '2024-06-16',
        'priority': 'high',
        'tag': 'family',
        'title': 'Call mom',
        'user_name': 'eve'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception("'priority' must be an integer")):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': "'priority' must be an integer"}

# Test Case 6: Create task with priority below allowed minimum
def test_create_task_with_priority_below_minimum():
    payload = {
        'description': 'Priority too low',
        'due_date': '2024-06-18',
        'priority': 0,
        'tag': 'test',
        'title': 'Test minimum priority',
        'user_name': 'frank'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception("'priority' must be between 1 and 5")):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': "'priority' must be between 1 and 5"}

# Test Case 7: Create task with priority above allowed maximum
def test_create_task_with_priority_above_maximum():
    payload = {
        'description': 'Priority too high',
        'due_date': '2024-06-18',
        'priority': 6,
        'tag': 'test',
        'title': 'Test maximum priority',
        'user_name': 'grace'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception("'priority' must be between 1 and 5")):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': "'priority' must be between 1 and 5"}

# Test Case 8: Create task with invalid due_date format
def test_create_task_with_invalid_due_date_format():
    payload = {
        'description': 'Wrong date format',
        'due_date': '18-06-2024',
        'priority': 3,
        'tag': 'test',
        'title': 'Test invalid due date',
        'user_name': 'hannah'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception("'due_date' must be in 'YYYY-MM-DD' format")):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': "'due_date' must be in 'YYYY-MM-DD' format"}

# Test Case 9: Create task with past due_date
def test_create_task_with_past_due_date():
    payload = {
        'description': 'Due date has already passed',
        'due_date': '2020-01-01',
        'priority': 2,
        'tag': 'test',
        'title': 'Test past due date',
        'user_name': 'ian'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception("'due_date' cannot be in the past")):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': "'due_date' cannot be in the past"}

# Test Case 10: Create task with maximum allowed title length
def test_create_task_with_maximum_allowed_title_length():
    title = 'T' * 255
    payload = {
        'description': 'Max length title test',
        'due_date': '2024-06-30',
        'priority': 4,
        'tag': 'long',
        'title': title,
        'user_name': 'jane'
    }
    expected = make_task_response(payload)
    with patch('app.services.task_service.TaskService.create_task', return_value=Task(**expected)):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 201
    assert response.json() == expected

# Test Case 11: Create task with title exceeding maximum length
def test_create_task_with_title_exceeding_maximum_length():
    title = 'T' * 256
    payload = {
        'description': 'Title too long',
        'due_date': '2024-06-25',
        'priority': 2,
        'tag': 'error',
        'title': title,
        'user_name': 'kate'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception("'title' length must not exceed 255 characters")):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': "'title' length must not exceed 255 characters"}

# Test Case 12: Create task with missing body
def test_create_task_with_missing_body():
    payload = {}
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception('Request body is required')):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': 'Request body is required'}

# Test Case 13: Create task with extra, unexpected field
def test_create_task_with_extra_unexpected_field():
    payload = {
        'description': 'Read a new novel',
        'due_date': '2024-06-22',
        'priority': 2,
        'tag': 'leisure',
        'title': 'Read book',
        'unexpected_field': 'unexpected_value',
        'user_name': 'leo'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception("Unexpected field 'unexpected_field' in request")):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': "Unexpected field 'unexpected_field' in request"}

# Test Case 14: Create task without authentication
def test_create_task_without_authentication():
    payload = {
        'description': 'Testing without auth headers',
        'due_date': '2024-06-23',
        'priority': 1,
        'tag': 'test',
        'title': 'No auth test',
        'user_name': 'mike'
    }
    expected = make_task_response(payload)
    with patch('app.services.task_service.TaskService.create_task', return_value=Task(**expected)):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 201
    assert response.json() == expected

# Test Case 15: Create task with HTML/script in description
def test_create_task_with_html_script_in_description():
    payload = {
        'description': "<script>alert('x')</script>",
        'due_date': '2024-06-24',
        'priority': 3,
        'tag': 'security',
        'title': 'HTML injection test',
        'user_name': 'nancy'
    }
    expected = make_task_response(payload)
    with patch('app.services.task_service.TaskService.create_task', return_value=Task(**expected)):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 201
    assert response.json() == expected

# Test Case 16: Create task with null fields
def test_create_task_with_null_fields():
    payload = {
        'description': None,
        'due_date': None,
        'priority': None,
        'tag': None,
        'title': None,
        'user_name': None
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception("Fields 'title', 'priority', 'due_date', and 'user_name' cannot be null")):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': "Fields 'title', 'priority', 'due_date', and 'user_name' cannot be null"}

# Test Case 17: Create task with only optional fields
def test_create_task_with_only_optional_fields():
    payload = {
        'description': 'No required fields',
        'tag': 'optional'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception('Missing required fields: title, priority, due_date, user_name')):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'detail': 'Missing required fields: title, priority, due_date, user_name'}

# Test Case 18: Create task with special characters in tag
def test_create_task_with_special_characters_in_tag():
    payload = {
        'description': 'Test special characters in tag',
        'due_date': '2024-06-28',
        'priority': 2,
        'tag': '@urgent#now!',
        'title': 'Special tag test',
        'user_name': 'oliver'
    }
    expected = make_task_response(payload)
    with patch('app.services.task_service.TaskService.create_task', return_value=Task(**expected)):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 201
    assert response.json() == expected