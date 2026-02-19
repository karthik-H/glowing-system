import pytest
from app.repositories.task_repository import TaskRepository

@pytest.fixture
def repo():
    return TaskRepository()

def test_add_task_with_all_valid_fields_location_ames(repo, caplog):
    """Test adding a task with all required fields and valid location 'ames'."""
    request_body = {
        'description': 'Milk, Bread, Eggs',
        'due_date': '2024-07-01',
        'location': 'ames',
        'priority': 'high',
        'title': 'Buy groceries',
        'user_name': 'alice'
    }
    caplog.set_level("INFO")
    response, code = repo.add_task(request_body)
    assert code == 201
    assert response['confirmation'] == 'Task created successfully.'
    task = response['task']
    assert task['description'] == request_body['description']
    assert task['due_date'] == request_body['due_date']
    assert task['location'] == request_body['location']
    assert task['priority'] == request_body['priority']
    assert task['title'] == request_body['title']
    assert task['user_name'] == request_body['user_name']
    assert 'id' in task
    assert "Task created:" in caplog.text

def test_add_task_with_all_valid_fields_location_boone(repo, caplog):
    """Test adding a task with all required fields and valid location 'boone'."""
    request_body = {
        'description': 'Project status meeting',
        'due_date': '2024-07-10',
        'location': 'boone',
        'priority': 'medium',
        'title': 'Meeting',
        'user_name': 'bob'
    }
    caplog.set_level("INFO")
    response, code = repo.add_task(request_body)
    assert code == 201
    assert response['confirmation'] == 'Task created successfully.'
    task = response['task']
    assert task['description'] == request_body['description']
    assert task['due_date'] == request_body['due_date']
    assert task['location'] == request_body['location']
    assert task['priority'] == request_body['priority']
    assert task['title'] == request_body['title']
    assert task['user_name'] == request_body['user_name']
    assert 'id' in task
    assert "Task created:" in caplog.text

def test_add_task_with_invalid_location(repo):
    """Test adding a task with an invalid location value."""
    request_body = {
        'description': 'Fix the kitchen sink',
        'due_date': '2024-07-05',
        'location': 'desmoines',
        'priority': 'low',
        'title': 'Call plumber',
        'user_name': 'carol'
    }
    response, code = repo.add_task(request_body)
    assert code == 400
    assert response['error'] == "Invalid location. Must be 'ames' or 'boone'."

def test_add_task_missing_title(repo):
    """Test adding a task with the required 'title' field missing."""
    request_body = {
        'description': 'No title provided',
        'due_date': '2024-07-12',
        'location': 'ames',
        'priority': 'high',
        'user_name': 'dave'
    }
    response, code = repo.add_task(request_body)
    assert code == 400
    assert response['error'] == 'Missing required field: title'

def test_add_task_missing_description(repo):
    """Test adding a task with the required 'description' field missing."""
    request_body = {
        'due_date': '2024-07-20',
        'location': 'boone',
        'priority': 'low',
        'title': 'Laundry',
        'user_name': 'eve'
    }
    response, code = repo.add_task(request_body)
    assert code == 400
    assert response['error'] == 'Missing required field: description'

def test_add_task_missing_priority(repo):
    """Test adding a task with the required 'priority' field missing."""
    request_body = {
        'description': 'Electricity and water',
        'due_date': '2024-07-03',
        'location': 'ames',
        'title': 'Pay bills',
        'user_name': 'frank'
    }
    response, code = repo.add_task(request_body)
    assert code == 400
    assert response['error'] == 'Missing required field: priority'

def test_add_task_missing_due_date(repo):
    """Test adding a task with the required 'due_date' field missing."""
    request_body = {
        'description': 'Annual checkup',
        'location': 'boone',
        'priority': 'medium',
        'title': 'Dentist appointment',
        'user_name': 'grace'
    }
    response, code = repo.add_task(request_body)
    assert code == 400
    assert response['error'] == 'Missing required field: due_date'

def test_add_task_missing_user_name(repo):
    """Test adding a task with the required 'user_name' field missing."""
    request_body = {
        'description': 'Change oil',
        'due_date': '2024-07-15',
        'location': 'ames',
        'priority': 'high',
        'title': 'Car maintenance'
    }
    response, code = repo.add_task(request_body)
    assert code == 400
    assert response['error'] == 'Missing required field: user_name'

def test_add_task_missing_location(repo):
    """Test adding a task with the required 'location' field missing."""
    request_body = {
        'description': 'At local restaurant',
        'due_date': '2024-07-08',
        'priority': 'medium',
        'title': 'Team lunch',
        'user_name': 'hannah'
    }
    response, code = repo.add_task(request_body)
    assert code == 400
    assert response['error'] == 'Missing required field: location'

def test_add_task_with_empty_title(repo, caplog):
    """Test adding a task where the 'title' field is an empty string (edge case)."""
    request_body = {
        'description': 'No title text',
        'due_date': '2024-07-02',
        'location': 'ames',
        'priority': 'low',
        'title': '',
        'user_name': 'ian'
    }
    caplog.set_level("INFO")
    response, code = repo.add_task(request_body)
    assert code == 201
    assert response['confirmation'] == 'Task created successfully.'
    task = response['task']
    assert task['title'] == ''
    assert task['description'] == request_body['description']
    assert task['due_date'] == request_body['due_date']
    assert task['location'] == request_body['location']
    assert task['priority'] == request_body['priority']
    assert task['user_name'] == request_body['user_name']
    assert 'id' in task
    assert "Task created:" in caplog.text

def test_add_task_with_title_at_maximum_length(repo, caplog):
    """Test adding a task where the 'title' field is at the assumed maximum allowed length (255 characters)."""
    max_title = 'T' * 255
    request_body = {
        'description': 'Long title test',
        'due_date': '2024-07-18',
        'location': 'boone',
        'priority': 'medium',
        'title': max_title,
        'user_name': 'jane'
    }
    caplog.set_level("INFO")
    response, code = repo.add_task(request_body)
    assert code == 201
    assert response['confirmation'] == 'Task created successfully.'
    task = response['task']
    assert task['title'] == max_title
    assert task['description'] == request_body['description']
    assert task['due_date'] == request_body['due_date']
    assert task['location'] == request_body['location']
    assert task['priority'] == request_body['priority']
    assert task['user_name'] == request_body['user_name']
    assert 'id' in task
    assert "Task created:" in caplog.text

def test_add_task_with_extra_fields(repo, caplog):
    """Test adding a task with additional, non-required fields in the request body to verify they are ignored."""
    request_body = {
        'description': 'Before deadline',
        'due_date': '2024-07-30',
        'extra_field': 'should be ignored',
        'location': 'ames',
        'priority': 'high',
        'title': 'File taxes',
        'user_name': 'kate'
    }
    caplog.set_level("INFO")
    response, code = repo.add_task(request_body)
    assert code == 201
    assert response['confirmation'] == 'Task created successfully.'
    task = response['task']
    assert task['description'] == request_body['description']
    assert task['due_date'] == request_body['due_date']
    assert task['location'] == request_body['location']
    assert task['priority'] == request_body['priority']
    assert task['title'] == request_body['title']
    assert task['user_name'] == request_body['user_name']
    assert 'id' in task
    assert 'extra_field' not in task
    assert "Task created:" in caplog.text

def test_add_duplicate_task_same_content_new_id(repo, caplog):
    """Test adding the same task data twice to confirm a new task ID is assigned each time."""
    request_body = {
        'description': 'Finish reading novel',
        'due_date': '2024-07-21',
        'location': 'boone',
        'priority': 'medium',
        'title': 'Read book',
        'user_name': 'leo'
    }
    caplog.set_level("INFO")
    response1, code1 = repo.add_task(request_body)
    response2, code2 = repo.add_task(request_body)
    assert code1 == 201
    assert code2 == 201
    task1 = response1['task']
    task2 = response2['task']
    assert task1['id'] != task2['id']
    assert task1['description'] == request_body['description']
    assert task2['description'] == request_body['description']
    assert task1['title'] == request_body['title']
    assert task2['title'] == request_body['title']
    assert response1['confirmation'] == 'Task created successfully.'
    assert response2['confirmation'] == 'Task created successfully.'
    assert "Task created:" in caplog.text

def test_add_task_with_invalid_priority_type(repo):
    """Test adding a task where 'priority' is not a string but an integer."""
    request_body = {
        'description': 'Code review for PR#123',
        'due_date': '2024-07-14',
        'location': 'ames',
        'priority': 1,
        'title': 'Review code',
        'user_name': 'mary'
    }
    response, code = repo.add_task(request_body)
    assert code == 400
    assert response['error'] == 'Invalid data type for field: priority'

def test_add_task_with_invalid_due_date_format(repo):
    """Test adding a task where the due date is not in a recognized date format."""
    request_body = {
        'description': 'Resolve login bug',
        'due_date': '07-14-2024',
        'location': 'boone',
        'priority': 'high',
        'title': 'Fix bug',
        'user_name': 'nina'
    }
    response, code = repo.add_task(request_body)
    assert code == 400
    assert response['error'] == 'Invalid date format for field: due_date'