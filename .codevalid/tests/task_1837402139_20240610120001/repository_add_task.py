import pytest
from app.repositories.task_repository import TaskRepository
from app.domain.models.task import Task

def make_task_repo():
    # Reset TaskRepository state for each test
    TaskRepository._tasks = []
    TaskRepository._id_counter = 1
    return TaskRepository

@pytest.fixture(autouse=True)
def reset_repo():
    TaskRepository._tasks = []
    TaskRepository._id_counter = 1

def test_add_task_with_valid_input():
    repo = make_task_repo()
    task_data = {
        'description': 'Document the API endpoints.',
        'due_date': '2024-07-10',
        'priority': 2,
        'title': 'Write documentation',
        'user_name': 'alice'
    }
    task = repo.add_task(task_data)
    assert task.description == 'Document the API endpoints.'
    assert task.due_date == '2024-07-10'
    assert task.priority == 2
    assert task.title == 'Write documentation'
    assert task.user_name == 'alice'
    assert task.id == 1

def test_add_task_missing_title():
    repo = make_task_repo()
    task_data = {
        'description': 'Document the API endpoints.',
        'due_date': '2024-07-10',
        'priority': 2,
        'user_name': 'alice'
    }
    with pytest.raises(ValueError) as exc:
        repo.add_task(task_data)
    assert "'title' is a required field" in str(exc.value)

def test_add_task_missing_description():
    repo = make_task_repo()
    task_data = {
        'due_date': '2024-07-10',
        'priority': 2,
        'title': 'Write documentation',
        'user_name': 'alice'
    }
    with pytest.raises(ValueError) as exc:
        repo.add_task(task_data)
    assert "'description' is a required field" in str(exc.value)

def test_add_task_missing_priority():
    repo = make_task_repo()
    task_data = {
        'description': 'Document the API endpoints.',
        'due_date': '2024-07-10',
        'title': 'Write documentation',
        'user_name': 'alice'
    }
    with pytest.raises(ValueError) as exc:
        repo.add_task(task_data)
    assert "'priority' is a required field" in str(exc.value)

def test_add_task_missing_due_date():
    repo = make_task_repo()
    task_data = {
        'description': 'Document the API endpoints.',
        'priority': 2,
        'title': 'Write documentation',
        'user_name': 'alice'
    }
    with pytest.raises(ValueError) as exc:
        repo.add_task(task_data)
    assert "'due_date' is a required field" in str(exc.value)

def test_add_task_missing_user_name():
    repo = make_task_repo()
    task_data = {
        'description': 'Document the API endpoints.',
        'due_date': '2024-07-10',
        'priority': 2,
        'title': 'Write documentation'
    }
    with pytest.raises(ValueError) as exc:
        repo.add_task(task_data)
    assert "'user_name' is a required field" in str(exc.value)

def test_add_task_with_location_field():
    repo = make_task_repo()
    task_data = {
        'description': 'Document the API endpoints.',
        'due_date': '2024-07-10',
        'location': 'Office',
        'priority': 2,
        'title': 'Write documentation',
        'user_name': 'alice'
    }
    with pytest.raises(ValueError) as exc:
        repo.add_task(task_data)
    assert "'location' is not an allowed field" in str(exc.value)

def test_add_task_with_no_fields():
    repo = make_task_repo()
    task_data = {}
    with pytest.raises(ValueError) as exc:
        repo.add_task(task_data)
    assert 'Required fields missing: title, description, priority, due_date, user_name' in str(exc.value)

def test_add_task_title_min_length():
    repo = make_task_repo()
    task_data = {
        'description': 'Short title',
        'due_date': '2024-07-10',
        'priority': 1,
        'title': 'A',
        'user_name': 'bob'
    }
    task = repo.add_task(task_data)
    assert task.title == 'A'
    assert task.id == 2
    assert task.description == 'Short title'
    assert task.due_date == '2024-07-10'
    assert task.priority == 1
    assert task.user_name == 'bob'

def test_add_task_title_max_length():
    repo = make_task_repo()
    max_title = 'T' * 255
    task_data = {
        'description': 'Max length title',
        'due_date': '2024-07-10',
        'priority': 1,
        'title': max_title,
        'user_name': 'charlie'
    }
    task = repo.add_task(task_data)
    assert task.title == max_title
    assert task.id == 3
    assert task.description == 'Max length title'
    assert task.due_date == '2024-07-10'
    assert task.priority == 1
    assert task.user_name == 'charlie'

def test_add_task_priority_min():
    repo = make_task_repo()
    task_data = {
        'description': 'This is the lowest priority.',
        'due_date': '2024-07-10',
        'priority': 1,
        'title': 'Low priority',
        'user_name': 'dave'
    }
    task = repo.add_task(task_data)
    assert task.priority == 1
    assert task.id == 4
    assert task.description == 'This is the lowest priority.'
    assert task.due_date == '2024-07-10'
    assert task.title == 'Low priority'
    assert task.user_name == 'dave'

def test_add_task_priority_max():
    repo = make_task_repo()
    task_data = {
        'description': 'This is the highest priority.',
        'due_date': '2024-07-10',
        'priority': 5,
        'title': 'High priority',
        'user_name': 'eve'
    }
    task = repo.add_task(task_data)
    assert task.priority == 5
    assert task.id == 5
    assert task.description == 'This is the highest priority.'
    assert task.due_date == '2024-07-10'
    assert task.title == 'High priority'
    assert task.user_name == 'eve'

def test_add_task_priority_out_of_bounds():
    repo = make_task_repo()
    task_data = {
        'description': 'Priority is zero.',
        'due_date': '2024-07-10',
        'priority': 0,
        'title': 'Invalid priority',
        'user_name': 'frank'
    }
    with pytest.raises(ValueError) as exc:
        repo.add_task(task_data)
    assert "'priority' must be between 1 and 5" in str(exc.value)

def test_add_task_due_date_invalid_format():
    repo = make_task_repo()
    task_data = {
        'description': "Due date as '10-07-2024'.",
        'due_date': '10-07-2024',
        'priority': 3,
        'title': 'Bad date',
        'user_name': 'gina'
    }
    with pytest.raises(ValueError) as exc:
        repo.add_task(task_data)
    assert "'due_date' must be in ISO format (YYYY-MM-DD)" in str(exc.value)

def test_add_task_priority_as_string():
    repo = make_task_repo()
    task_data = {
        'description': "Priority is 'high'.",
        'due_date': '2024-07-10',
        'priority': 'high',
        'title': 'Priority string',
        'user_name': 'hugo'
    }
    with pytest.raises(ValueError) as exc:
        repo.add_task(task_data)
    assert "'priority' must be an integer" in str(exc.value)

def test_add_task_empty_title():
    repo = make_task_repo()
    task_data = {
        'description': 'No title provided.',
        'due_date': '2024-07-10',
        'priority': 2,
        'title': '',
        'user_name': 'ian'
    }
    with pytest.raises(ValueError) as exc:
        repo.add_task(task_data)
    assert "'title' must not be empty" in str(exc.value)

def test_add_task_duplicate_task():
    repo = make_task_repo()
    task_data = {
        'description': 'Same data',
        'due_date': '2024-07-10',
        'priority': 3,
        'title': 'Duplicate',
        'user_name': 'john'
    }
    task1 = repo.add_task(task_data)
    task2 = repo.add_task(task_data)
    assert task1.id == 6
    assert task2.id == 7
    assert task1.title == task2.title == 'Duplicate'
    assert task1.description == task2.description == 'Same data'
    assert task1.due_date == task2.due_date == '2024-07-10'
    assert task1.priority == task2.priority == 3
    assert task1.user_name == task2.user_name == 'john'