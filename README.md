# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
🐾 Initializing PawPal System...

Registered pets for Sarah Connor: Buster (Dog), Luna (Cat)

Successfully scheduled 3 tasks across pets.

==================================================
📅 TODAY'S SCHEDULE & SMART PLAN
==================================================

💡 Successfully organized 3 tasks for Sarah Connor. Prioritized using urgency levels and checked against the daily time limit (240 mins).

--------------------------------------------------
1. [HIGH] Brisk 45-minute walk around the neighborhood park. (08:30 AM)
   • Pet: Buster
   • Category: Walk | Duration: 45 mins
   • Details: Brisk 45-minute walk around the neighborhood park.
--------------------------------------------------
2. [MEDIUM] Feed wet food and fresh water. (09:00 AM)
   • Pet: Luna
   • Category: Feeding | Duration: 15 mins
   • Details: Feed wet food and fresh water.
--------------------------------------------------
3. [LOW] Coat brushing and dental check. (06:00 PM)
   • Pet: Buster
   • Category: Grooming | Duration: 20 mins
   • Details: Coat brushing and dental check.
--------------------------------------------------
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python3 -m pytest

Covers: 
   ~ State & Mutation: Basic task completion (test_task_completion) and household collection tracking (test_task_addition_increases_count).

   ~ Core Algorithms: Chronological task sorting (test_sorting_correctness).

   ~ Automation & Safety: Automated recurring task generation (test_recurrence_logic_daily_task) and non-blocking time conflict detection (test_conflict_detection_flags_overlapping_times).

# Run with coverage:
pytest --cov
```

Sample test output:

```
Kahlyns-MacBook-Air:ai110-module2show-pawpal-starter kahlynblackshear$ python3 -m pytest
============================= test session starts =============================
platform darwin -- Python 3.14.7, pytest-9.1.1, pluggy-1.6.0
rootdir: /Users/kahlynblackshear/Documents/GitHub/ai110-module2show-pawpal-starter
plugins: anyio-4.14.2
collected 5 items                                                             

tests/test_pawpal.py .....                                              [100%]

============================== 5 passed in 0.03s ==============================
```
Confidence Level: 5 Stars

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_by_time(), Scheduler.generate_daily_plan() | Organizes tasks chronologically and resolves ties using weighted priority levels. |
| Filtering | Scheduler.filter_tasks() | Optimized single-pass filter that simultaneously queries tasks by completion status and/or pet name.|
| Conflict handling | Scheduler.check_time_conflict(), Scheduler.schedule_task() | Performs lightweight interval overlap detection and uses a non-blocking warning approach so owners can manually double-book during emergencies. |
| Recurring tasks | Scheduler.complete_task() | Automatically generates and schedules the next task instance when a "Daily" or "Weekly" task is marked completed. |

## 📸 Demo Walkthrough

Describe your app in numbered steps so a reader can follow along without watching a video:

1. Household Setup & Registering Pets:
Use the sidebar to configure your owner profile and register pets. Provide a Pet ID, name, species (Dog, Cat, etc.), and optional special notes (e.g., high energy or medication requirements).
2. Adding Tasks via Quick Task Creator:
In the main dashboard, select a registered pet from the dropdown, then fill out the task parameters—including description, category (Walk, Feeding, Meds, Grooming, Enrichment), duration in minutes, priority level (High, Medium, Low), and scheduled time.
3. Triggering Conflict Warnings:
Attempt to schedule a task that overlaps with an existing time slot (e.g., adding a medical appointment at 8:45 AM when a 45-minute walk is already running from 8:30 AM). The scheduler will instantly intercept the action and display an in-app warning banner flagging the time conflict.
4. Filtering and Sorting Household Tasks:
Scroll down to the Current Household Tasks table. Use the filter dropdowns to isolate tasks by completion status (Pending or Completed) or by individual pets. The application automatically sorts tasks in chronological order.
5. Generating the Optimized Daily Plan:
Click Generate Schedule to let the system synthesize your tasks against household preferences. Expandable results provide a prioritized itinerary with breakdown details for every task and pet.

Sample CLI Output:
```
🐾 Initializing PawPal System...

Registered pets for Sarah Connor: Buster (Dog), Luna (Cat)

============================================================
⚠️ TESTING CONFLICT DETECTION DURING SCHEDULING
============================================================
⚠️ Warning: Task 't4' (Urgent vet consultation call) overlaps with 't1' (Brisk 45-minute walk around the neighborhood park.).

Successfully processed all tasks.

============================================================
⏰ TESTING SORT_BY_TIME() METHOD (Chronological Order)
============================================================
1. [08:30 AM] Brisk 45-minute walk around the neighborhood park. - Pet: Buster
2. [08:45 AM] Urgent vet consultation call. - Pet: Luna
3. [09:00 AM] Feed wet food and fresh water. - Pet: Luna
4. [06:00 PM] Coat brushing and dental check. - Pet: Buster

============================================================
📅 TODAY'S SCHEDULE & SMART PLAN
============================================================

💡 Generated optimized schedule prioritizing high-constraint items and managing daily duration limits.

------------------------------------------------------------
1. [HIGH] Brisk 45-minute walk around the neighborhood park. (08:30 AM)
   • Pet: Buster
   • Category: Walk | Duration: 45 mins
------------------------------------------------------------
2. [HIGH] Urgent vet consultation call. (08:45 AM)
   • Pet: Luna
   • Category: Medical | Duration: 30 mins
------------------------------------------------------------
3. [MEDIUM] Feed wet food and fresh water. (09:00 AM)
   • Pet: Luna
   • Category: Feeding | Duration: 15 mins
------------------------------------------------------------
4. [LOW] Coat brushing and dental check. (06:00 PM)
   • Pet: Buster
   • Category: Grooming | Duration: 20 mins
------------------------------------------------------------
```

## Features 
🐾 PawPal+ Core Features & Algorithms
⚡ Non-Blocking Time Conflict Warnings

Algorithm: Utilizes an interval overlap formula (new_start < exist_end) and (new_end > exist_start) to evaluate prospective task windows against all existing household tasks.

UX: Instantly flags schedule collisions via Streamlit warnings while allowing the pet owner the flexibility to proceed if intentional.

⏰ Chronological Task Sorting

Algorithm: Implements Python's efficient sorted() function with a custom lambda key (key=lambda task: task.scheduled_time) to automatically organize tasks in sequential order from morning to night.

🔍 Optimized Single-Pass Filtering

Algorithm: Processes multi-criteria filters concurrently in a single list-comprehension pass, evaluating both task completion status (is_completed) and pet ownership (pet_name) without redundant data iterations.

🔄 Automated Recurring Task Generation

Algorithm: Triggered upon task completion (complete_task), this feature calculates future occurrences using Python's timedelta (adding exactly 1 day for daily tasks or 7 days for weekly tasks), automatically appending the next iteration to the schedule with a unique dynamic ID.

⚖️ Weighted Priority Daily Plan Generation

Algorithm: Evaluates today’s tasks using a composite sorting key that cross-references user-defined priority weights (High, Medium, Low) alongside chronological schedules, ensuring urgent care needs always float to the top of the daily plan.

🏠 Multi-Pet Household Management

Architecture: Built around a robust aggregate data structure where a central Owner class manages multiple Pet entities, cleanly isolating pets, special notes, and care duties under a single household account.

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
