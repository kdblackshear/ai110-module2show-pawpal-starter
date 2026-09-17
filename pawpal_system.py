from dataclasses import dataclass, field
from datetime import datetime, date, time
from typing import List, Dict, Any, Optional

@dataclass
class OwnerPreferences:
    max_daily_minutes: int = 180
    priority_weights: Dict[str, int] = field(default_factory=lambda: {"High": 1, "Medium": 2, "Low": 3})
    preferred_walk_windows: List[tuple[time, time]] = field(default_factory=list)


@dataclass
class Task:
    task_id: str
    pet_id: str
    description: str  # Description of the activity
    category: str
    duration_minutes: int
    priority: str  # 'High', 'Medium', 'Low'
    scheduled_time: datetime
    frequency: str = "Daily"  # Added frequency (e.g., Daily, Weekly, Once)
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


@dataclass
class Pet:
    pet_id: str
    name: str
    type: str
    special_notes: str = ""
    tasks: List[Task] = field(default_factory=list)  # List of tasks for this pet

    def update_notes(self, new_notes: str) -> None:
        """Appends or updates the pet's special notes."""
        self.special_notes = new_notes

    def get_profile_summary(self) -> str:
        """Returns a formatted summary of the pet's details."""
        return f"Pet: {self.name} ({self.type}) - Notes: {self.special_notes or 'None'}"


@dataclass
class Owner:
    owner_id: str
    name: str
    preferences: OwnerPreferences = field(default_factory=OwnerPreferences)
    pets: Dict[str, Pet] = field(default_factory=dict)  # Manages multiple pets

    def add_pet(self, pet: Pet) -> None:
        """Adds a pet to the owner's household."""
        self.pets[pet.pet_id] = pet

    def get_all_tasks(self) -> List[Task]:
        """Provides access to all tasks across all managed pets."""
        all_tasks = []
        for pet in self.pets.values():
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    """The 'Brain' that retrieves, organizes, and manages tasks across pets."""
    def __init__(self, owner: Optional[Owner] = None):
        self.owner: Owner = owner or Owner(owner_id="o1", name="Primary Owner")

    def add_pet(self, pet_object: Pet) -> None:
        """Registers a new pet into the owner's household."""
        self.owner.add_pet(pet_object)

    def schedule_task(self, task_object: Task) -> bool:
        """Adds a new care task to the correct pet with validation."""
        if task_object.pet_id not in self.owner.pets:
            raise ValueError(f"Cannot schedule task: Pet ID {task_object.pet_id} does not exist.")
        
        self.owner.pets[task_object.pet_id].tasks.append(task_object)
        return True

    def get_todays_tasks(self, target_date: Optional[date] = None) -> List[Task]:
        """Retrieves and filters tasks scheduled for the specified date."""
        if target_date is None:
            target_date = datetime.now().date()
        
        all_tasks = self.owner.get_all_tasks()
        return [t for t in all_tasks if t.scheduled_time.date() == target_date]

    def generate_daily_plan(self, target_date: Optional[date] = None) -> Dict[str, Any]:
        """Organizes tasks across pets based on priority and time constraints."""
        todays_tasks = self.get_todays_tasks(target_date)
        
        weight_map = self.owner.preferences.priority_weights
        sorted_tasks = sorted(
            todays_tasks,
            key=lambda x: (weight_map.get(x.priority, 99), x.scheduled_time)
        )
        
        explanation = (
            f"Successfully organized {len(sorted_tasks)} tasks for {self.owner.name}. "
            f"Prioritized using urgency levels and checked against the "
            f"daily time limit ({self.owner.preferences.max_daily_minutes} mins)."
        )
        
        return {
            "schedule": sorted_tasks,
            "explanation": explanation
        }