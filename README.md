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
pytest

# Run with coverage:
pytest --cov
```

Sample test output:

```
# Paste your pytest output here
```

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

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
