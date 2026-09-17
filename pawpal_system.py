from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Dict, Any, Optional

@dataclass
class Pet:
    pet_id: str
    name: str
    type: str
    special_notes: str = ""
    tasks: List['Task'] = field(default_factory=list)  # Added bi-directional relationship

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
    def __init__(self):
        self.pets: Dict[str, Pet] = {}
        self.tasks: List[Task] = []
        # Structured constraints rather than a vague dictionary
        self.constraints: Dict[str, Any] = {
            "max_daily_minutes": 180,
            "priority_weights": {"High": 1, "Medium": 2, "Low": 3}
        }

    def add_pet(self, pet_object: Pet) -> None:
        """Registers a new pet into the manager."""
        self.pets[pet_object.pet_id] = pet_object

    def schedule_task(self, task_object: Task) -> bool:
        """Adds a new care task to the queue with validation."""
        if task_object.pet_id not in self.pets:
            raise ValueError(f"Cannot schedule task: Pet ID {task_object.pet_id} does not exist.")
        
        # Check for exact time overlap for the same pet
        for t in self.tasks:
            if t.pet_id == task_object.pet_id and t.scheduled_time == task_object.scheduled_time:
                print(f"Warning: Multiple tasks scheduled at {task_object.scheduled_time} for pet {task_object.pet_id}.")

        self.tasks.append(task_object)
        # Automatically sync the task to the specific pet object as well
        self.pets[task_object.pet_id].tasks.append(task_object)
        return True

    def get_todays_tasks(self, target_date: Optional[date] = None) -> List[Task]:
        """Filters and returns tasks scheduled for the specified date (defaults to today)."""
        if target_date is None:
            target_date = datetime.now().date()
        return [t for t in self.tasks if t.scheduled_time.date() == target_date]

    def generate_daily_plan(self, target_date: Optional[date] = None) -> Dict[str, Any]:
        """Applies priority weights and constraints to build an optimized daily schedule."""
        todays_tasks = self.get_todays_tasks(target_date)
        
        # Sort tasks: Primary by priority weight, Secondary by scheduled time
        weight_map = self.constraints.get("priority_weights", {"High": 1, "Medium": 2, "Low": 3})
        sorted_tasks = sorted(
            todays_tasks,
            key=lambda x: (weight_map.get(x.priority, 99), x.scheduled_time)
        )
        
        explanation = (
            f"Successfully organized {len(sorted_tasks)} tasks for the day. "
            "Tasks were prioritized by urgency level (High -> Medium -> Low) "
            "and then ordered chronologically by scheduled time."
        )
        
        return {
            "schedule": sorted_tasks,
            "explanation": explanation
        }