import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from task import Task


def test_task_initial_attributes():
    task = Task("Plant Corn #1", "PLANT", (3, 1), duration=3)
    assert task.get_name() == "Plant Corn #1"
    assert task.get_type() == "PLANT"
    assert task.get_position() == (3, 1)
    assert task.get_duration() == 3
    assert task.get_progress() == 0
    assert task.get_status() == "WAITING"


def test_task_invalid_duration_raises_error():
    with pytest.raises(ValueError):
        Task("Bad Task", "PLANT", (0, 0), duration=0)


def test_task_status_validation():
    task = Task("Water Rice #1", "WATER", (4, 2), duration=2)
    task.set_status("IN_PROGRESS")
    assert task.get_status() == "IN_PROGRESS"

    with pytest.raises(ValueError):
        task.set_status("UNKNOWN")


def test_task_advance_progress_completes_at_duration():
    task = Task("Water Rice #1", "WATER", (4, 2), duration=2)
    task.set_status("IN_PROGRESS")

    assert task.advance_progress() is False
    assert task.get_progress() == 1
    assert task.get_status() == "IN_PROGRESS"

    assert task.advance_progress() is True
    assert task.get_progress() == 2
    assert task.get_status() == "DONE"