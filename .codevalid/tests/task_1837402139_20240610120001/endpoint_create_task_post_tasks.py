import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.domain.models.task import Task
from unittest.mock import patch

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_tasks():
    # In real tests, clear DB or mock repository here
    pass

# Test Case 1: create_task_with_all_fields_location_ames
def test_create_task_with_all_fields_location_ames():
    payload = {
        'description': 'Purchase milk, eggs, and bread',
        'due_date': '2024-07-01T12:00:00Z',
        'location': 'ames',
        'priority': 'high',
        'title': 'Buy groceries',
        'user_name': 'john_doe'
    }
    expected = payload.copy()
    with patch('app.services.task_service.TaskService.create_task', return_value=Task(**expected)):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 201
    assert response.json() == expected

# Test Case 2: create_task_with_all_fields_location_boone
def test_create_task_with_all_fields_location_boone():
    payload = {
        'description': 'Complete the API test cases',
        'due_date': '2024-06-30',
        'location': 'boone',
        'priority': 2,
        'title': 'Finish assignment',
        'user_name': 'alice'
    }
    expected = payload.copy()
    with patch('app.services.task_service.TaskService.create_task', return_value=Task(**expected)):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 201
    assert response.json() == expected

# Test Case 3: create_task_with_invalid_location
def test_create_task_with_invalid_location():
    payload = {
        'description': 'Reminder to call mom',
        'due_date': '2024-07-03',
        'location': 'desmoines',
        'priority': 'medium',
        'title': 'Call mom',
        'user_name': 'bob'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception("Invalid location: must be 'ames' or 'boone'.")):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'error': "Invalid location: must be 'ames' or 'boone'."}

# Test Case 4: create_task_missing_title
def test_create_task_missing_title():
    payload = {
        'description': 'No title here',
        'due_date': '2024-08-01',
        'location': 'ames',
        'priority': 'low',
        'user_name': 'jane'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception('Missing required field: title')):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'error': 'Missing required field: title'}

# Test Case 5: create_task_missing_description
def test_create_task_missing_description():
    payload = {
        'due_date': '2024-07-10',
        'location': 'boone',
        'priority': 'medium',
        'title': 'Read book',
        'user_name': 'emma'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception('Missing required field: description')):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'error': 'Missing required field: description'}

# Test Case 6: create_task_missing_priority
def test_create_task_missing_priority():
    payload = {
        'description': 'Evening walk',
        'due_date': '2024-07-05',
        'location': 'ames',
        'title': 'Walk dog',
        'user_name': 'lisa'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception('Missing required field: priority')):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'error': 'Missing required field: priority'}

# Test Case 7: create_task_missing_due_date
def test_create_task_missing_due_date():
    payload = {
        'description': 'Feed the cat before work',
        'location': 'boone',
        'priority': 'high',
        'title': 'Feed cat',
        'user_name': 'maria'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception('Missing required field: due_date')):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'error': 'Missing required field: due_date'}

# Test Case 8: create_task_missing_user_name
def test_create_task_missing_user_name():
    payload = {
        'description': 'Tidy up bedroom',
        'due_date': '2024-07-09',
        'location': 'ames',
        'priority': 'low',
        'title': 'Clean room'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception('Missing required field: user_name')):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'error': 'Missing required field: user_name'}

# Test Case 9: create_task_missing_location
def test_create_task_missing_location():
    payload = {
        'description': 'Electricity and water',
        'due_date': '2024-07-02',
        'priority': 'high',
        'title': 'Pay bills',
        'user_name': 'steve'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception('Missing required field: location')):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'error': 'Missing required field: location'}

# Test Case 10: create_task_with_empty_title
def test_create_task_with_empty_title():
    payload = {
        'description': 'Empty title test',
        'due_date': '2024-07-15',
        'location': 'boone',
        'priority': 'low',
        'title': '',
        'user_name': 'testuser'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception('Title cannot be empty.')):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'error': 'Title cannot be empty.'}

# Test Case 11: create_task_priority_as_string_number
def test_create_task_priority_as_string_number():
    payload = {
        'description': 'Priority as string number',
        'due_date': '2024-07-12',
        'location': 'ames',
        'priority': '1',
        'title': 'Test priority',
        'user_name': 'bob'
    }
    expected = payload.copy()
    with patch('app.services.task_service.TaskService.create_task', return_value=Task(**expected)):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 201
    assert response.json() == expected

# Test Case 12: create_task_priority_as_integer
def test_create_task_priority_as_integer():
    payload = {
        'description': 'Priority as integer',
        'due_date': '2024-07-14',
        'location': 'boone',
        'priority': 3,
        'title': 'Integer priority',
        'user_name': 'carol'
    }
    expected = payload.copy()
    with patch('app.services.task_service.TaskService.create_task', return_value=Task(**expected)):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 201
    assert response.json() == expected

# Test Case 13: create_task_due_date_iso8601
def test_create_task_due_date_iso8601():
    payload = {
        'description': 'Due date as ISO 8601 string',
        'due_date': '2024-07-20T16:00:00Z',
        'location': 'ames',
        'priority': 'medium',
        'title': 'ISO due date',
        'user_name': 'dan'
    }
    expected = payload.copy()
    with patch('app.services.task_service.TaskService.create_task', return_value=Task(**expected)):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 201
    assert response.json() == expected

# Test Case 14: create_task_due_date_invalid_format
def test_create_task_due_date_invalid_format():
    payload = {
        'description': 'Invalid due date format',
        'due_date': '07/30/2024',
        'location': 'boone',
        'priority': 'high',
        'title': 'Bad due date',
        'user_name': 'eve'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception('Invalid due_date format. Use ISO 8601.')):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'error': 'Invalid due_date format. Use ISO 8601.'}

# Test Case 15: create_task_location_case_sensitivity
def test_create_task_location_case_sensitivity():
    payload = {
        'description': 'Test location case sensitivity',
        'due_date': '2024-07-18',
        'location': 'Ames',
        'priority': 'low',
        'title': 'Case test',
        'user_name': 'frank'
    }
    with patch('app.services.task_service.TaskService.create_task', side_effect=Exception("Invalid location: must be 'ames' or 'boone'.")):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 400
    assert response.json() == {'error': "Invalid location: must be 'ames' or 'boone'."}

# Test Case 16: create_task_with_additional_field
def test_create_task_with_additional_field():
    payload = {
        'description': 'Extra field should be ignored',
        'due_date': '2024-07-19',
        'extraField': 'shouldBeIgnored',
        'location': 'ames',
        'priority': 'medium',
        'title': 'With extra',
        'user_name': 'harry'
    }
    expected = payload.copy()
    expected.pop('extraField')
    with patch('app.services.task_service.TaskService.create_task', return_value=Task(**expected)):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 201
    assert response.json() == expected

# Test Case 17: create_task_with_large_title
def test_create_task_with_large_title():
    title = 'T' * 255
    payload = {
        'description': 'Long title string of 255 chars',
        'due_date': '2024-07-25',
        'location': 'boone',
        'priority': 'high',
        'title': title,
        'user_name': 'longtitleuser'
    }
    expected = payload.copy()
    with patch('app.services.task_service.TaskService.create_task', return_value=Task(**expected)):
        response = client.post('/tasks', json=payload)
    assert response.status_code == 201
    assert response.json() == expected