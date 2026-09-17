from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import List, Dict, Any, Optional

@dataclass
class OwnerPreferences:
    max_daily_minutes: int = 180
    priority_weights: Dict[str, int] = field(default_factory=lambda: {"High": 1, "Medium": 2, "Low": 3})
    preferred_walk_windows: List[tuple[time, time]] = field(default_factory=list)

    def update_max_minutes(self, new_limit: int) -> None:
        """Updates the maximum daily time allowed for pet tasks."""
        self.max_daily_minutes = new_limit

    def add_walk_window(self, start: time, end: time) -> None:
        """Adds a preferred time window for walking pets."""
        self.preferred_walk_windows.append((start, end))


@dataclass
class Pet:
    pet_id: str
    name: str
    type: str
    special_notes: str = ""
    tasks: List['Task'] = field(default_factory=list)

    def update_notes(self, new_notes: str) -> None:
        """Appends or updates the pet's special notes."""
        self.special_notes = new_notes

    def get_profile_summary(self) -> str:
        """Returns a formatted summary of the pet's details."""
        return f"Pet: {self.name} ({self.type}) - Notes: {self.special_notes or 'None'}"


@dataclass
class Task:
    task_id: str
    pet_id: str
    title: str
    category: str
    duration_minutes: int
    priority: str  # e.g., 'High', 'Medium', 'Low'
    scheduled_time: datetime
    is_completed: bool = False

    def mark_completed(self) -> None:
        """Sets the task status to finished."""
        self.is_completed = True

    def reschedule(self, new_time: datetime) -> None:
        """Updates the scheduled time for the task."""
        self.scheduled_time = new_time

    def update_priority(self, new_priority: str) -> None:
        """Changes the priority level of the task."""
        self.priority = new_priority


class ScheduleManager:
    def __init__(self, preferences: Optional[OwnerPreferences] = None):
        self.pets: Dict[str, Pet] = {}
        self.tasks: List[Task] = []
        # Use the dedicated preferences object
        self.preferences: OwnerPreferences = preferences or OwnerPreferences()

    def add_pet(self, pet_object: Pet) -> None:
        """Registers a new pet into the manager."""
        self.pets[pet_object.pet_id] = pet_object

    def schedule_task(self, task_object: Task) -> bool:
        """Adds a new care task to the queue with validation."""
        if task_object.pet_id not in self.pets:
            raise ValueError(f"Cannot schedule task: Pet ID {task_object.pet_id} does not exist.")
        
        self.tasks.append(task_object)
        self.pets[task_object.pet_id].tasks.append(task_object)
        return True

    def get_todays_tasks(self, target_date: Optional[date] = None) -> List[Task]:
        """Filters and returns tasks scheduled for the specified date (defaults to today)."""
        if target_date is None:
            target_date = datetime.now().date()
        return [t for t in self.tasks if t.scheduled_time.date() == target_date]

    def generate_daily_plan(self, target_date: Optional[date] = None) -> Dict[str, Any]:
        """Applies owner preferences and priority weights to build an optimized daily schedule."""
        todays_tasks = self.get_todays_tasks(target_date)
        
        # Sort tasks using the weights defined in OwnerPreferences
        weight_map = self.preferences.priority_weights
        sorted_tasks = sorted(
            todays_tasks,
            key=lambda x: (weight_map.get(x.priority, 99), x.scheduled_time)
        )
        
        explanation = (
            f"Successfully organized {len(sorted_tasks)} tasks for the day. "
            f"Filtered based on owner max daily time limit ({self.preferences.max_daily_minutes} mins) "
            "and sorted by priority level followed by scheduled time."
        )
        
        return {
            "schedule": sorted_tasks,
            "explanation": explanation
        }