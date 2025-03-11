# Intervals Time Tracking Scripts

This repository contains scripts for interacting with the Intervals API, specifically for tracking time on the "Meeting Tracker Internal Project" task.

## Setup

1. Make sure you have Python installed on your system.
2. Install the required dependencies:
   ```
   pip install requests
   ```
3. The scripts use your Intervals API key (7ghfnbbbo6s) which is already configured.

## Available Scripts

### post_time.py

This script allows you to post time to the Meeting Tracker Internal Project task.

#### Usage

```
python post_time.py [options]
```

#### Options

- `--task-id`: Task ID (default: 16474442 - Meeting Tracker Internal Project)
- `--time`: Time in decimal hours (default: 1.00)
- `--date`: Date in YYYY-MM-DD format (default: today)
- `--description`: Description of work (default: empty)
- `--billable`: Mark time as billable (default: false)

#### Examples

Post 1 hour of time to the Meeting Tracker Internal Project task with a description:
```
python post_time.py --description "Meeting with team to discuss project progress"
```

Post 2.5 hours of time on a specific date:
```
python post_time.py --time 2.50 --date 2025-03-10 --description "Extended team meeting"
```

### intervals_api.py

This is a Python wrapper for the Intervals API that provides methods for interacting with various endpoints.

#### Usage

```python
from intervals_api import IntervalsAPI

# Initialize the API with your API key
api = IntervalsAPI("7ghfnbbbo6s")

# Get your user information
user_info = api.get_me()
person_id = user_info['me'][0]['id']

# Post time to a task
response = api.create_time(
    task_id="16474442",  # Meeting Tracker Internal Project
    person_id=person_id,
    date="2025-03-11",
    time_value="1.00",
    work_type_id="305064",  # India-Meeting
    description="Meeting with team",
    billable=False
)

# Check if the time was posted successfully
if response.get("status") == "Created" and response.get("code") == 201:
    print("Time posted successfully!")
    print(f"Time Entry ID: {response.get('time', {}).get('id')}")
else:
    print(f"Error posting time: {response}")
```

## Other Scripts

- `find_worktype.py`: Script to find work type IDs for projects
- `view_tasks_example.py`: Script to view tasks in your Intervals account
- `get_task_by_id_example.py`: Script to get details of a specific task by ID

## Important IDs

- Task ID for Meeting Tracker Internal Project: 16474442
- Work Type ID for India-Meeting: 305064
- Project ID for Internal: 959242

## Notes

- The scripts automatically use your user ID when posting time
- Time must be entered in decimal format (e.g., "1.00" for 1 hour, "1.50" for 1 hour and 30 minutes)
- The API returns status code 201 (Created) when time is successfully posted 