# PawPal+ Project Reflection

## 1. System Design

        A user should be able to add a pet, schedule a task (walk, feeding, grooming, etc.), and see the entirety of the day's scheduled tasks.

        To do this, we would need the classes:
            1. Pet:
                ~ Attributes: 
                    - pet_id
                    - name
                    - type
                    - special_notes
                ~ Methods: 
                    - update_notes(new_notes)
                    - get_profile_summary()
            2. Task:
                ~ Attributes:
                    - task_id
                    - pet_id
                    - title
                    - category
                    - duration_minutes
                    - priority
                    - scheduled_time
                    - is_completed
                ~ Methods: 
                    - mark_completed()
                    - reschedule(new_time)
                    - update_priority(new_priority)
            3. ScheduleManager:
                ~ Attributes: 
                    - pets
                    - tasks
                    - constraints
                ~ Methods:
                    - add_pet(pet_object)
                    - schedule_task(task_object)
                    - get_todays_tasks()
                    - generate_daily_plan()

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to each?

        The initial UML design has the relationships: 
            - ScheduleManager to Pet (1-to-many): The manager holds a collection of pets registered in the application.
            - ScheduleManager to Task (1-to-many): The manager holds and processes all scheduled care tasks across all pets.
            - ScheduleManager to OwnerPreferences (1-to-1): The manager holds a single instance of OwnerPreferences. When generate_daily_plan() runs, it directly consults these preferences (like max_daily_minutes and priority_weights) to shape the output.

        I chose the classes OwnerProferences, Pet, Task, and ScheduleManager. OwnerPreferences holds the responsibility of setting time limits, prioryt weights, and preferred walk windows, as well as helper actions to each task. Pet holds the responsibility of gathering important information (name, id, type, etc.) about each pet that needs to be cared for. Task holds the responsibility of adding tasks tied to each pet as well as giving each a scheduled time and priority. It also allows for each task to be marked completed when done. ScheduleManager holds the resposibility of adding new pets and tasks to the daily schdule. It also generates a daily plan with all taks that need to get done that day. 

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

        Yes, after asking my AI agent to look for pitfall in the code, one of the suggestions it made was to add data validation on schdeuling. There is now a check inside schedule_task() to verify that pet_id exists before it adds a task, this prevents adding a task for a non-existent pet.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

        One of the tradeoffs that my scheduler makes is that instead of outright rejecting an overlapping task, it will print a warning message and add the task anyway. This is reasonable for this scenario because it makes the scheduler more flexible for the user, which most aligns with daily life that has unexpected events, like emergency vet visits that may override a scheduled walk.  
---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
