import pytest
from app.repositories.task_repository import TaskRepository
from app.domain.models.task import Task, TaskCreate
from pydantic import ValidationError
from datetime import date

@pytest.fixture
def repo():
    return TaskRepository()

def make_taskcreate(data):
    # Helper to handle missing fields and None values
    return TaskCreate(**data)

def test_add_task_with_all_fields_provided(repo, caplog):
    data = {
        "title": "Buy groceries",
        "description": "Milk, Bread, Eggs",
        "priority": 3,
        "due_date": date(2024, 7, 15),
        "user_name": "alice"
    }
    caplog.set_level("INFO")
    task = repo.add_task(make_taskcreate(data))
    assert task.id == 1
    assert repo._id_counter == 2
    assert repo._tasks == [task]
    assert task.dict() == {**data, "id": 1}
    assert "Task created: " in caplog.text

def test_add_task_missing_optional_fields(repo, caplog):
    # All fields are required in TaskCreate, so this should fail
    data = {
        "title": "Call Bob"
    }
    with pytest.raises(ValidationError) as exc:
        make_taskcreate(data)
    assert "field required" in str(exc.value)

def test_add_task_with_empty_string_fields(repo, caplog):
    data = {
        "title": "",
        "description": "",
        "priority": 1,
        "due_date": "",
        "user_name": ""
    }
    # due_date as empty string will fail validation
    with pytest.raises(ValidationError) as exc:
        make_taskcreate(data)
    assert "value is not a valid date" in str(exc.value) or "ensure this value has at least 1 characters" in str(exc.value)

def test_add_task_with_invalid_priority_value(repo, caplog):
    data = {
        "title": "Feed cat",
        "description": "Feed cat food",
        "priority": "urgent",
        "due_date": date(2024, 7, 15),
        "user_name": "bob"
    }
    # priority as string will fail validation
    with pytest.raises(ValidationError) as exc:
        make_taskcreate(data)
    assert "value is not a valid integer" in str(exc.value)

def test_add_task_with_invalid_due_date_format(repo, caplog):
    data = {
        "title": "Complete report",
        "description": "Finish Q2 report",
        "priority": 2,
        "due_date": "15-07-2024",
        "user_name": "carol"
    }
    # due_date as string in wrong format will fail validation
    with pytest.raises(ValidationError) as exc:
        make_taskcreate(data)
    assert "value is not a valid date" in str(exc.value)

def test_add_task_with_duplicate_title(repo, caplog):
    data1 = {
        "title": "Read book",
        "description": "1984 by George Orwell",
        "priority": 2,
        "due_date": date(2024, 7, 20),
        "user_name": "alice"
    }
    data2 = {
        "title": "Read book",
        "description": "Brave New World",
        "priority": 2,
        "due_date": date(2024, 7, 21),
        "user_name": "bob"
    }
    caplog.set_level("INFO")
    task1 = repo.add_task(make_taskcreate(data1))
    task2 = repo.add_task(make_taskcreate(data2))
    assert task1.id == 1
    assert task2.id == 2
    assert repo._id_counter == 3
    assert repo._tasks == [task1, task2]
    assert "Task created: " in caplog.text

def test_add_task_missing_title_field(repo):
    data = {
        "description": "Laundry",
        "priority": 1,
        "due_date": date(2024, 7, 15),
        "user_name": "alice"
    }
    with pytest.raises(ValidationError) as exc:
        make_taskcreate(data)
    assert "field required" in str(exc.value)

def test_add_task_with_non_string_field_values(repo):
    data = {
        "title": 123,
        "description": ["list", "of", "descriptions"],
        "priority": True,
        "due_date": None,
        "user_name": 456
    }
    with pytest.raises(ValidationError) as exc:
        make_taskcreate(data)
    assert "value is not a valid string" in str(exc.value) or "value is not a valid date" in str(exc.value)

def test_add_task_with_large_input_fields(repo):
    data = {
        "title": "T" * 255,
        "description": "D" * 1024,
        "priority": 5,
        "due_date": date(2024, 12, 31),
        "user_name": "U" * 255
    }
    with pytest.raises(ValidationError) as exc:
        make_taskcreate(data)
    # Should fail due to max_length constraints
    assert "ensure this value has at most" in str(exc.value)

def test_add_task_with_special_characters(repo, caplog):
    data = {
        "title": "✨ Urgent! ✨",
        "description": "Fix bug #123 🚨",
        "priority": 3,
        "due_date": date(2024, 8, 8),
        "user_name": "李华"
    }
    caplog.set_level("INFO")
    task = repo.add_task(make_taskcreate(data))
    assert task.id == 1
    assert repo._id_counter == 2
    assert repo._tasks == [task]
    assert task.dict() == {**data, "id": 1}
    assert "Task created: " in caplog.text