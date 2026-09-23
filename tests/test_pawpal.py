from datetime import datetime, timedelta
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


def test_sorting_correctness():
    """Verify tasks are returned in chronological order by sort_by_time()."""
    # Arrange
    pet = Pet(pet_id="p1", name="Rex", type="Dog")
    scheduler = Scheduler()
    scheduler.add_pet(pet)
    
    t_late = Task(task_id="t1", pet_id="p1", description="Evening Walk", category="Walk", duration_minutes=30, priority="Low", scheduled_time=datetime(2026, 6, 1, 18, 0))
    t_early = Task(task_id="t2", pet_id="p1", description="Morning Feed", category="Food", duration_minutes=15, priority="High", scheduled_time=datetime(2026, 6, 1, 7, 30))
    t_mid = Task(task_id="t3", pet_id="p1", description="Midday Play", category="Play", duration_minutes=30, priority="Medium", scheduled_time=datetime(2026, 6, 1, 12, 0))
    
    pet.tasks.extend([t_late, t_early, t_mid])
    
    # Act
    sorted_tasks = scheduler.sort_by_time()
    
    # Assert
    assert [t.task_id for t in sorted_tasks] == ["t2", "t3", "t1"]


def test_recurrence_logic_daily_task():
    """Confirm that marking a daily task complete creates a new task for the following day."""
    # Arrange
    pet = Pet(pet_id="p1", name="Buster", type="Dog")
    scheduler = Scheduler()
    scheduler.add_pet(pet)
    
    original_time = datetime(2026, 6, 1, 8, 0, 0)
    task = Task(
        task_id="task_daily",
        pet_id="p1",
        description="Morning Jog",
        category="Exercise",
        duration_minutes=45,
        priority="High",
        scheduled_time=original_time,
        frequency="Daily",
        is_completed=False
    )
    scheduler.schedule_task(task)
    
    # Act
    next_task = scheduler.complete_task("task_daily")
    
    # Assert
    assert task.is_completed is True
    assert next_task is not None
    assert next_task.scheduled_time == original_time + timedelta(days=1)
    assert next_task.is_completed is False
    assert next_task in pet.tasks


def test_conflict_detection_flags_overlapping_times():
    """Verify that the Scheduler flags duplicate or overlapping times."""
    # Arrange
    pet = Pet(pet_id="p1", name="Max", type="Dog")
    scheduler = Scheduler()
    scheduler.add_pet(pet)
    
    # Task 1: 10:00 AM to 11:00 AM
    task1 = Task(
        task_id="t1",
        pet_id="p1",
        description="Grooming",
        category="Care",
        duration_minutes=60,
        priority="Medium",
        scheduled_time=datetime(2026, 6, 1, 10, 0, 0)
    )
    scheduler.schedule_task(task1)
    
    # Task 2: 10:30 AM to 11:00 AM (Overlaps with Task 1)
    task2 = Task(
        task_id="t2",
        pet_id="p1",
        description="Vet Checkup",
        category="Medical",
        duration_minutes=30,
        priority="High",
        scheduled_time=datetime(2026, 6, 1, 10, 30, 0)
    )
    
    # Act
    warning = scheduler.check_time_conflict(task2)
    
    # Assert
    assert warning is not None
    assert "overlaps with" in warning
    assert "Grooming" in warning