from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any

@dataclass
class Pet:
    pet_id: str
    name: str
    type: str
    special_notes: str = ""

    def update_notes(self, new_notes: str) -> None:
        """Appends or updates the pet's special notes."""
        pass

    def get_profile_summary(self) -> str:
        """Returns a formatted summary of the pet's details."""
        pass


@dataclass
class Task:
    task_id: str
    pet_id: str
    title: str
    category: str
    duration_minutes: int
    priority: str
    scheduled_time: datetime
    is_completed: bool = False

    def mark_completed(self) -> None:
        """Sets the task status to finished."""
        pass

    def reschedule(self, new_time: datetime) -> None:
        """Updates the scheduled time for the task."""
        pass

    def update_priority(self, new_priority: str) -> None:
        """Changes the priority level of the task."""
        pass


class ScheduleManager:
    def __init__(self):
        self.pets: Dict[str, Pet] = {}
        self.tasks: List[Task] = []
        self.constraints: Dict[str, Any] = {}

    def add_pet(self, pet_object: Pet) -> None:
        """Registers a new pet into the manager."""
        pass

    def schedule_task(self, task_object: Task) -> None:
        """Adds a new care task to the queue."""
        pass

    def get_todays_tasks(self) -> List[Task]:
        """Filters and returns tasks scheduled for the current day."""
        pass

    def generate_daily_plan(self) -> Dict[str, Any]:
        """Applies constraints and priority rules to build an optimized daily schedule."""
        pass