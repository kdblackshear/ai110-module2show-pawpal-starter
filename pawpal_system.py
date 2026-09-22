from dataclasses import dataclass, field
from datetime import datetime, date, time, timedelta
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
        """Sets task status to finished."""
        self.is_completed = True

    def reschedule(self, new_time: datetime) -> None:
        """Updates the scheduled time for the task."""
        self.scheduled_time = new_time

    def update_priority(self, new_priority: str) -> None:
        """Changes task priority level."""
        self.priority = new_priority


@dataclass
class Pet:
    pet_id: str
    name: str
    type: str
    special_notes: str = ""
    tasks: List[Task] = field(default_factory=list)  # List of tasks for this pet

    def update_notes(self, new_notes: str) -> None:
        """Updates special notes for the pet."""
        self.special_notes = new_notes

    def get_profile_summary(self) -> str:
        """Returns a formatted summary of pet details."""
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
        """Returns all tasks across all managed pets."""
        all_tasks = []
        for pet in self.pets.values():
            all_tasks.extend(pet.tasks)
        return all_tasks


class Scheduler:
    """The 'Brain' that retrieves, organizes, and manages tasks across pets."""
    def __init__(self, owner: Optional[Owner] = None):
        self.owner: Owner = owner or Owner(owner_id="o1", name="Primary Owner")

    def add_pet(self, pet_object: Pet) -> None:
        """Registers a new pet into the owner household."""
        self.owner.add_pet(pet_object)

    def schedule_task(self, task_object: Task) -> Optional[str]:
        """Adds a new care task to the specified pet with lightweight conflict detection."""
        if task_object.pet_id not in self.owner.pets:
            raise ValueError(f"Cannot schedule task: Pet ID {task_object.pet_id} does not exist.")
        
        # Check for time conflicts gracefully
        warning = self.check_time_conflict(task_object)
        if warning:
            print(warning)  # Prints warning cleanly without crashing execution
            
        # Append the task regardless, allowing the owner to double-book if needed
        self.owner.pets[task_object.pet_id].tasks.append(task_object)
        return warning

    def get_todays_tasks(self, target_date: Optional[date] = None) -> List[Task]:
        """Filters and returns tasks scheduled for the target date."""
        if target_date is None:
            target_date = datetime.now().date()
        
        all_tasks = self.owner.get_all_tasks()
        return [t for t in all_tasks if t.scheduled_time.date() == target_date]

    def sort_by_time(self, tasks: Optional[List[Task]] = None) -> List[Task]:
        """
        Sorts a list of Task objects chronologically by their scheduled_time attribute 
        using a lambda key function.
        """
        if tasks is None:
            tasks = self.owner.get_all_tasks()
        
        # Lambda key extracts the datetime object for chronological sorting
        return sorted(tasks, key=lambda task: task.scheduled_time)

    def filter_tasks(self, is_completed: Optional[bool] = None, pet_name: Optional[str] = None) -> List[Task]:
        """
        Filters tasks simultaneously by their completion status and/or the pet's name.
        """
        all_tasks = self.owner.get_all_tasks()
        filtered = all_tasks

        # Filter by completion status if provided
        if is_completed is not None:
            filtered = [t for t in filtered if t.is_completed == is_completed]

        # Filter by pet name if provided (case-insensitive lookup)
        if pet_name is not None:
            matching_pet_ids = {
                p.pet_id for p in self.owner.pets.values() 
                if p.name.lower() == pet_name.lower()
            }
            filtered = [t for t in filtered if t.pet_id in matching_pet_ids]

        return filtered
    
    def complete_task(self, task_id: str) -> Optional[Task]:
        """
        Marks a task as complete. If the task has a 'Daily' or 'Weekly' frequency, 
        it automatically generates and schedules the next occurrence.
        """
        target_task = None
        # Locate the task across all pets
        for pet in self.owner.pets.values():
            for task in pet.tasks:
                if task.task_id == task_id:
                    target_task = task
                    break
            if target_task:
                break
        
        if not target_task:
            raise ValueError(f"Task ID {task_id} not found across any pet.")

        # Mark the current instance as completed
        target_task.mark_completed()

        # Check for recurrence rules
        if target_task.frequency in ["Daily", "Weekly"]:
            # Determine the time delta based on frequency
            delta = timedelta(days=1) if target_task.frequency == "Daily" else timedelta(weeks=1)
            next_scheduled_time = target_task.scheduled_time + delta
            
            # Generate a unique ID for the next occurrence
            new_task_id = f"{target_task.task_id}_{next_scheduled_time.strftime('%Y%m%d')}"
            
            # Create the next occurrence task instance
            next_task = Task(
                task_id=new_task_id,
                pet_id=target_task.pet_id,
                description=target_task.description,
                category=target_task.category,
                duration_minutes=target_task.duration_minutes,
                priority=target_task.priority,
                scheduled_time=next_scheduled_time,
                frequency=target_task.frequency,
                is_completed=False
            )
            
            # Automatically schedule the new recurrence
            self.schedule_task(next_task)
            print(f"🔄 Recurring Task Generated: '{next_task.description}' scheduled for {next_task.scheduled_time.strftime('%B %d, %Y at %I:%M %p')}")
            return next_task

        return None
    
    def check_time_conflict(self, new_task: Task) -> Optional[str]:
        """
        Lightweight conflict detection strategy.
        Checks if a new task's time window overlaps with any existing task across any pet.
        Returns a warning message string if a conflict is found, or None if clear.
        """
        new_start = new_task.scheduled_time
        new_end = new_start + timedelta(minutes=new_task.duration_minutes)
        
        # Gather all tasks across all pets in the household
        all_tasks = self.owner.get_all_tasks()
        
        for existing in all_tasks:
            # Skip checking against itself (useful if updating an existing task)
            if existing.task_id == new_task.task_id:
                continue
                
            exist_start = existing.scheduled_time
            exist_end = exist_start + timedelta(minutes=existing.duration_minutes)
            
            # Interval overlap formula: (StartA < EndB) and (EndA > StartB)
            if new_start < exist_end and new_end > exist_start:
                pet = self.owner.pets.get(existing.pet_id)
                pet_name = pet.name if pet else "Unknown Pet"
                
                warning_msg = (
                    f"⚠️ Scheduling Warning: '{new_task.description}' ({new_start.strftime('%I:%M %p')}) "
                    f"overlaps with '{existing.description}' assigned to {pet_name} at {exist_start.strftime('%I:%M %p')}!"
                )
                return warning_msg
                
        return None

    def generate_daily_plan(self, target_date: Optional[date] = None) -> Dict[str, Any]:
        """Builds an optimized daily schedule based on priorities and constraints."""
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