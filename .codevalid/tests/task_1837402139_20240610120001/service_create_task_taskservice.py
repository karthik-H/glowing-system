import pytest
from unittest.mock import MagicMock, patch
from app.services.task_service import TaskService
from app.domain.models.task import TaskCreate, Task
from datetime import date

@pytest.fixture
def mock_repository():
    repo = MagicMock()
    repo.add_task = MagicMock()
    return repo

@pytest.fixture
def task_service(mock_repository):
    return TaskService(repository=mock_repository)

@pytest.fixture
def logger_patch():
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        yield logger

# Test Case 1: test_create_task_success_ames
def test_create_task_success_ames(task_service, mock_repository, logger_patch):
    data = {
        "description": "Purchase milk, eggs, and bread.",
        "due_date": "2024-06-25",
        "location": "ames",
        "priority": "high",
        "title": "Buy groceries",
        "user_name": "alice"
    }
    task_data = TaskCreate(**data)
    created_task = Task(**data)
    mock_repository.add_task.return_value = created_task
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        result = task_service.create_task(task_data)
        logger.info.assert_called_once_with("Creating task for user: alice")
    mock_repository.add_task.assert_called_once_with(task_data)
    assert result == created_task

# Test Case 2: test_create_task_success_boone
def test_create_task_success_boone(task_service, mock_repository, logger_patch):
    data = {
        "description": "Jog for 30 minutes.",
        "due_date": "2024-06-26",
        "location": "boone",
        "priority": "medium",
        "title": "Morning run",
        "user_name": "bob"
    }
    task_data = TaskCreate(**data)
    created_task = Task(**data)
    mock_repository.add_task.return_value = created_task
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        result = task_service.create_task(task_data)
        logger.info.assert_called_once_with("Creating task for user: bob")
    mock_repository.add_task.assert_called_once_with(task_data)
    assert result == created_task

# Test Case 3: test_create_task_invalid_location
def test_create_task_invalid_location(task_service, mock_repository, logger_patch):
    data = {
        "description": "Read new novel.",
        "due_date": "2024-06-27",
        "location": "des moines",
        "priority": "low",
        "title": "Read Book",
        "user_name": "carol"
    }
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        with pytest.raises(ValueError) as exc:
            task_service.create_task(TaskCreate(**data))
        assert str(exc.value) == "Invalid location. Must be 'ames' or 'boone'."
        logger.info.assert_not_called()
    mock_repository.add_task.assert_not_called()

# Test Case 4: test_create_task_missing_title
def test_create_task_missing_title(task_service, mock_repository, logger_patch):
    data = {
        "description": "Walk the dog.",
        "due_date": "2024-06-28",
        "location": "ames",
        "priority": "medium",
        "user_name": "dan"
    }
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        with pytest.raises(ValueError) as exc:
            task_service.create_task(TaskCreate(**data))
        assert str(exc.value) == "Missing required field: title"
        logger.info.assert_not_called()
    mock_repository.add_task.assert_not_called()

# Test Case 5: test_create_task_missing_description
def test_create_task_missing_description(task_service, mock_repository, logger_patch):
    data = {
        "due_date": "2024-06-29",
        "location": "boone",
        "priority": "low",
        "title": "Laundry",
        "user_name": "eve"
    }
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        with pytest.raises(ValueError) as exc:
            task_service.create_task(TaskCreate(**data))
        assert str(exc.value) == "Missing required field: description"
        logger.info.assert_not_called()
    mock_repository.add_task.assert_not_called()

# Test Case 6: test_create_task_missing_priority
def test_create_task_missing_priority(task_service, mock_repository, logger_patch):
    data = {
        "description": "Electricity and water bills.",
        "due_date": "2024-06-30",
        "location": "ames",
        "title": "Pay bills",
        "user_name": "frank"
    }
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        with pytest.raises(ValueError) as exc:
            task_service.create_task(TaskCreate(**data))
        assert str(exc.value) == "Missing required field: priority"
        logger.info.assert_not_called()
    mock_repository.add_task.assert_not_called()

# Test Case 7: test_create_task_missing_due_date
def test_create_task_missing_due_date(task_service, mock_repository, logger_patch):
    data = {
        "description": "Weekly check-in.",
        "location": "boone",
        "priority": "high",
        "title": "Call mom",
        "user_name": "grace"
    }
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        with pytest.raises(ValueError) as exc:
            task_service.create_task(TaskCreate(**data))
        assert str(exc.value) == "Missing required field: due_date"
        logger.info.assert_not_called()
    mock_repository.add_task.assert_not_called()

# Test Case 8: test_create_task_missing_user_name
def test_create_task_missing_user_name(task_service, mock_repository, logger_patch):
    data = {
        "description": "Gym session.",
        "due_date": "2024-07-01",
        "location": "ames",
        "priority": "medium",
        "title": "Workout"
    }
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        with pytest.raises(ValueError) as exc:
            task_service.create_task(TaskCreate(**data))
        assert str(exc.value) == "Missing required field: user_name"
        logger.info.assert_not_called()
    mock_repository.add_task.assert_not_called()

# Test Case 9: test_create_task_missing_location
def test_create_task_missing_location(task_service, mock_repository, logger_patch):
    data = {
        "description": "Prepare for exams.",
        "due_date": "2024-07-02",
        "priority": "high",
        "title": "Study",
        "user_name": "hannah"
    }
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        with pytest.raises(ValueError) as exc:
            task_service.create_task(TaskCreate(**data))
        assert str(exc.value) == "Missing required field: location"
        logger.info.assert_not_called()
    mock_repository.add_task.assert_not_called()

# Test Case 10: test_create_task_empty_fields
def test_create_task_empty_fields(task_service, mock_repository, logger_patch):
    data = {}
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        with pytest.raises(ValueError) as exc:
            task_service.create_task(TaskCreate(**data))
        assert str(exc.value) == "Missing required field: title"
        logger.info.assert_not_called()
    mock_repository.add_task.assert_not_called()

# Test Case 11: test_create_task_boundary_title_length
def test_create_task_boundary_title_length(task_service, mock_repository, logger_patch):
    long_title = "T" * 255
    data = {
        "description": "Boundary title length test.",
        "due_date": "2024-07-03",
        "location": "boone",
        "priority": "low",
        "title": long_title,
        "user_name": "ivy"
    }
    task_data = TaskCreate(**data)
    created_task = Task(**data)
    mock_repository.add_task.return_value = created_task
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        result = task_service.create_task(task_data)
        logger.info.assert_called_once_with("Creating task for user: ivy")
    mock_repository.add_task.assert_called_once_with(task_data)
    assert result == created_task

# Test Case 12: test_create_task_boundary_due_date_format
def test_create_task_boundary_due_date_format(task_service, mock_repository, logger_patch):
    data = {
        "description": "Backup important files.",
        "due_date": "07-04-2024",
        "location": "ames",
        "priority": "medium",
        "title": "Backup files",
        "user_name": "jack"
    }
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        with pytest.raises(ValueError) as exc:
            task_service.create_task(TaskCreate(**data))
        assert str(exc.value) == "Invalid due_date format. Expected YYYY-MM-DD."
        logger.info.assert_not_called()
    mock_repository.add_task.assert_not_called()

# Test Case 13: test_create_task_extra_unexpected_fields
def test_create_task_extra_unexpected_fields(task_service, mock_repository, logger_patch):
    data = {
        "description": "Spring cleaning.",
        "due_date": "2024-07-05",
        "location": "boone",
        "priority": "low",
        "title": "Clean garage",
        "unexpected_field": "extra_data",
        "user_name": "kate"
    }
    # Only expected fields should be used
    expected_data = {k: v for k, v in data.items() if k in ["description", "due_date", "location", "priority", "title", "user_name"]}
    task_data = TaskCreate(**expected_data)
    created_task = Task(**expected_data)
    mock_repository.add_task.return_value = created_task
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        result = task_service.create_task(task_data)
        logger.info.assert_called_once_with("Creating task for user: kate")
    mock_repository.add_task.assert_called_once_with(task_data)
    assert result == created_task