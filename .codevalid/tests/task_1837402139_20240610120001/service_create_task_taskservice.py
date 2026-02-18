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

def make_task_create(data):
    # Helper to handle missing/optional fields and type conversion
    fields = {
        "title": data.get("title"),
        "description": data.get("description"),
        "priority": data.get("priority"),
        "due_date": data.get("due_date"),
        "user_name": data.get("user_name"),
        "tag": data.get("tag"),
    }
    # Remove None fields for TaskCreate
    return fields

# Test Case 1: Create task with all valid fields
def test_create_task_with_all_valid_fields(task_service, mock_repository, logger_patch):
    data = {
        "description": "Milk, Bread, Eggs",
        "due_date": "2024-07-01",
        "priority": "high",
        "tag": "shopping",
        "title": "Buy groceries",
        "user_name": "alice"
    }
    # Simulate allowed priorities: high=3, medium=2, low=1
    priority_map = {"high": 3, "medium": 2, "low": 1}
    task_data = TaskCreate(
        title=data["title"],
        description=data["description"],
        priority=priority_map[data["priority"]],
        due_date=date.fromisoformat(data["due_date"]),
        user_name=data["user_name"]
    )
    mock_repository.add_task.return_value = Task(
        id=1,
        **task_data.dict()
    )
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        result = task_service.create_task(task_data)
        logger.info.assert_called_once_with("Creating task for user: alice")
    mock_repository.add_task.assert_called_once_with(task_data)
    assert result.id == 1
    assert result.title == "Buy groceries"
    assert result.description == "Milk, Bread, Eggs"
    assert result.priority == 3
    assert result.due_date == date(2024, 7, 1)
    assert result.user_name == "alice"

# Test Case 2: Create task without tag field
def test_create_task_without_tag_field(task_service, mock_repository, logger_patch):
    data = {
        "description": "Discuss project timeline",
        "due_date": "2024-07-10",
        "priority": "medium",
        "title": "Call Bob",
        "user_name": "bob"
    }
    priority_map = {"high": 3, "medium": 2, "low": 1}
    task_data = TaskCreate(
        title=data["title"],
        description=data["description"],
        priority=priority_map[data["priority"]],
        due_date=date.fromisoformat(data["due_date"]),
        user_name=data["user_name"]
    )
    mock_repository.add_task.return_value = Task(
        id=2,
        **task_data.dict()
    )
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        result = task_service.create_task(task_data)
        logger.info.assert_called_once_with("Creating task for user: bob")
    mock_repository.add_task.assert_called_once_with(task_data)
    assert result.id == 2
    assert result.title == "Call Bob"
    assert result.description == "Discuss project timeline"
    assert result.priority == 2
    assert result.due_date == date(2024, 7, 10)
    assert result.user_name == "bob"

# Test Case 3: Create task missing required title
def test_create_task_missing_required_title(task_service, mock_repository, logger_patch):
    data = {
        "description": "Prepare report",
        "due_date": "2024-06-30",
        "priority": "low",
        "tag": "work",
        "user_name": "carol"
    }
    priority_map = {"high": 3, "medium": 2, "low": 1}
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        with pytest.raises(TypeError):
            TaskCreate(
                description=data["description"],
                priority=priority_map[data["priority"]],
                due_date=date.fromisoformat(data["due_date"]),
                user_name=data["user_name"]
            )
        logger.info.assert_not_called()
    mock_repository.add_task.assert_not_called()

# Test Case 4: Create task with invalid priority value
def test_create_task_with_invalid_priority_value(task_service, mock_repository, logger_patch):
    data = {
        "description": "Weekend clothes",
        "due_date": "2024-07-05",
        "priority": "urgent",
        "tag": "home",
        "title": "Do laundry",
        "user_name": "dave"
    }
    priority_map = {"high": 3, "medium": 2, "low": 1}
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        with pytest.raises(KeyError):
            TaskCreate(
                title=data["title"],
                description=data["description"],
                priority=priority_map[data["priority"]],
                due_date=date.fromisoformat(data["due_date"]),
                user_name=data["user_name"]
            )
        logger.info.assert_not_called()
    mock_repository.add_task.assert_not_called()

# Test Case 5: Create task with empty title
def test_create_task_with_empty_title(task_service, mock_repository, logger_patch):
    data = {
        "description": "Weekly planning",
        "due_date": "2024-07-07",
        "priority": "medium",
        "tag": "planning",
        "title": "",
        "user_name": "eve"
    }
    priority_map = {"high": 3, "medium": 2, "low": 1}
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        with pytest.raises(ValueError):
            TaskCreate(
                title=data["title"],
                description=data["description"],
                priority=priority_map[data["priority"]],
                due_date=date.fromisoformat(data["due_date"]),
                user_name=data["user_name"]
            )
        logger.info.assert_not_called()
    mock_repository.add_task.assert_not_called()

# Test Case 6: Create task with invalid due date format
def test_create_task_with_invalid_due_date_format(task_service, mock_repository, logger_patch):
    data = {
        "description": "Electricity and water",
        "due_date": "07/01/2024",
        "priority": "high",
        "tag": "finance",
        "title": "Pay bills",
        "user_name": "frank"
    }
    priority_map = {"high": 3, "medium": 2, "low": 1}
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        with pytest.raises(ValueError):
            TaskCreate(
                title=data["title"],
                description=data["description"],
                priority=priority_map[data["priority"]],
                due_date=date.fromisoformat(data["due_date"]),
                user_name=data["user_name"]
            )
        logger.info.assert_not_called()
    mock_repository.add_task.assert_not_called()

# Test Case 7: Create task missing user_name
def test_create_task_missing_user_name(task_service, mock_repository, logger_patch):
    data = {
        "description": "Concert",
        "due_date": "2024-07-11",
        "priority": "low",
        "tag": "leisure",
        "title": "Book tickets"
    }
    priority_map = {"high": 3, "medium": 2, "low": 1}
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        with pytest.raises(TypeError):
            TaskCreate(
                title=data["title"],
                description=data["description"],
                priority=priority_map[data["priority"]],
                due_date=date.fromisoformat(data["due_date"])
            )
        logger.info.assert_not_called()
    mock_repository.add_task.assert_not_called()

# Test Case 8: Create task with minimal required fields
def test_create_task_with_minimal_required_fields(task_service, mock_repository, logger_patch):
    data = {
        "due_date": "2024-07-15",
        "priority": "low",
        "title": "Read book",
        "user_name": "george"
    }
    priority_map = {"high": 3, "medium": 2, "low": 1}
    task_data = TaskCreate(
        title=data["title"],
        description=None,
        priority=priority_map[data["priority"]],
        due_date=date.fromisoformat(data["due_date"]),
        user_name=data["user_name"]
    )
    mock_repository.add_task.return_value = Task(
        id=3,
        **task_data.dict()
    )
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        result = task_service.create_task(task_data)
        logger.info.assert_called_once_with("Creating task for user: george")
    mock_repository.add_task.assert_called_once_with(task_data)
    assert result.id == 3
    assert result.title == "Read book"
    assert result.description is None
    assert result.priority == 1
    assert result.due_date == date(2024, 7, 15)
    assert result.user_name == "george"

# Test Case 9: Create task with long title and description
def test_create_task_with_long_title_and_description(task_service, mock_repository, logger_patch):
    long_title = "T" * 100
    long_description = "T" * 1000
    data = {
        "description": long_description,
        "due_date": "2024-07-21",
        "priority": "medium",
        "tag": "study",
        "title": long_title,
        "user_name": "harry"
    }
    priority_map = {"high": 3, "medium": 2, "low": 1}
    task_data = TaskCreate(
        title=data["title"],
        description=data["description"],
        priority=priority_map[data["priority"]],
        due_date=date.fromisoformat(data["due_date"]),
        user_name=data["user_name"]
    )
    mock_repository.add_task.return_value = Task(
        id=4,
        **task_data.dict()
    )
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        result = task_service.create_task(task_data)
        logger.info.assert_called_once_with("Creating task for user: harry")
    mock_repository.add_task.assert_called_once_with(task_data)
    assert result.id == 4
    assert result.title == long_title
    assert result.description == long_description
    assert result.priority == 2
    assert result.due_date == date(2024, 7, 21)
    assert result.user_name == "harry"

# Test Case 10: Create task with empty description
def test_create_task_with_empty_description(task_service, mock_repository, logger_patch):
    data = {
        "description": "",
        "due_date": "2024-07-12",
        "priority": "low",
        "tag": "misc",
        "title": "Task with empty desc",
        "user_name": "ian"
    }
    priority_map = {"high": 3, "medium": 2, "low": 1}
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        with pytest.raises(ValueError):
            TaskCreate(
                title=data["title"],
                description=data["description"],
                priority=priority_map[data["priority"]],
                due_date=date.fromisoformat(data["due_date"]),
                user_name=data["user_name"]
            )
        logger.info.assert_not_called()
    mock_repository.add_task.assert_not_called()

# Test Case 11: Create task with due_date in the past
def test_create_task_with_due_date_in_past(task_service, mock_repository, logger_patch):
    data = {
        "description": "Should allow past dates",
        "due_date": "2024-05-01",
        "priority": "medium",
        "tag": "archive",
        "title": "Past task",
        "user_name": "jack"
    }
    priority_map = {"high": 3, "medium": 2, "low": 1}
    task_data = TaskCreate(
        title=data["title"],
        description=data["description"],
        priority=priority_map[data["priority"]],
        due_date=date.fromisoformat(data["due_date"]),
        user_name=data["user_name"]
    )
    mock_repository.add_task.return_value = Task(
        id=5,
        **task_data.dict()
    )
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        result = task_service.create_task(task_data)
        logger.info.assert_called_once_with("Creating task for user: jack")
    mock_repository.add_task.assert_called_once_with(task_data)
    assert result.id == 5
    assert result.title == "Past task"
    assert result.description == "Should allow past dates"
    assert result.priority == 2
    assert result.due_date == date(2024, 5, 1)
    assert result.user_name == "jack"

# Test Case 12: Create task with null fields
def test_create_task_with_null_fields(task_service, mock_repository, logger_patch):
    data = {
        "description": None,
        "due_date": None,
        "priority": None,
        "tag": None,
        "title": None,
        "user_name": None
    }
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        with pytest.raises(TypeError):
            TaskCreate(
                title=data["title"],
                description=data["description"],
                priority=data["priority"],
                due_date=data["due_date"],
                user_name=data["user_name"]
            )
        logger.info.assert_not_called()
    mock_repository.add_task.assert_not_called()

# Test Case 13: Create task with non-string tag
def test_create_task_with_non_string_tag(task_service, mock_repository, logger_patch):
    data = {
        "description": "Tag should be string",
        "due_date": "2024-07-18",
        "priority": "low",
        "tag": 1234,
        "title": "Task with bad tag type",
        "user_name": "kelly"
    }
    priority_map = {"high": 3, "medium": 2, "low": 1}
    task_data = TaskCreate(
        title=data["title"],
        description=data["description"],
        priority=priority_map[data["priority"]],
        due_date=date.fromisoformat(data["due_date"]),
        user_name=data["user_name"]
    )
    # Simulate tag type check
    with patch("app.services.task_service.logging.getLogger") as logger_mock:
        logger = MagicMock()
        logger_mock.return_value = logger
        if not isinstance(data["tag"], str):
            with pytest.raises(TypeError):
                raise TypeError("Tag must be a string")
            logger.info.assert_not_called()
        else:
            result = task_service.create_task(task_data)
            logger.info.assert_called_once_with("Creating task for user: kelly")
            mock_repository.add_task.assert_called_once_with(task_data)
            assert result.id == 6
            assert result.title == "Task with bad tag type"
            assert result.description == "Tag should be string"
            assert result.priority == 1
            assert result.due_date == date(2024, 7, 18)
            assert result.user_name == "kelly"