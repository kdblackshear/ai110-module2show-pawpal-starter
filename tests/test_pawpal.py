from datetime import datetime
from pawpal_system import Pet, Task, Scheduler

def test_task_completion():
    """Verify that calling mark_completed() changes the task's status to True."""
    # Arrange
    task = Task(
        task_id="t1",
        pet_id="p1",
        description="Evening Walk",
        category="Walk",
        duration_minutes=30,
        priority="High",
        scheduled_time=datetime.now(),
        is_completed=False
    )
    
    # Assert initial state
    assert task.is_completed is False
    
    # Act
    task.mark_completed()
    
    # Assert final state
    assert task.is_completed is True


def test_task_addition_increases_count():
    """Verify that adding a task to a Pet increases that pet's task count."""
    # Arrange
    pet = Pet(pet_id="p1", name="Buster", type="Dog")
    scheduler = Scheduler()
    scheduler.add_pet(pet)
    
    initial_count = len(pet.tasks)
    assert initial_count == 0
    
    # Act
    task = Task(
        task_id="t2",
        pet_id="p1",
        description="Feeding time",
        category="Feeding",
        duration_minutes=15,
        priority="Medium",
        scheduled_time=datetime.now()
    )
    scheduler.schedule_task(task)
    
    # Assert
    final_count = len(pet.tasks)
    assert final_count == initial_count + 1
    assert pet.tasks[0].task_id == "t2"