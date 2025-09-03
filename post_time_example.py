from intervals_api import IntervalsAPI
import json
from datetime import datetime

def main():
    # Your API key
    api_key = "2ee0xsyu0aw"
    
    # Create an instance of the IntervalsAPI class
    api = IntervalsAPI(api_key)
    
    # Task and work type details
    task_id = "16738168"  # Meeting Tracker Internal Project
    work_type_id = "304999"  # India-Meeting
    
    # Get user information to verify connection
    user_info = api.get_me()
    if user_info.get("status") != "OK":
        print(f"Error connecting to Intervals API: {user_info}")
        return
    
    person_id = user_info['me'][0]['id']
    print(f"Connected as: {user_info['me'][0]['firstname']} {user_info['me'][0]['lastname']} (ID: {person_id})")
    
    # Get the task details to confirm
    print(f"\nFetching task with ID: {task_id}...")
    task = api.get_task_by_id(task_id)
    
    if task.get("status") == "OK":
        task_data = task.get("task", {})
        print(f"Task: {task_data.get('title')}")
        print(f"Project: {task_data.get('project')}")
        print(f"Client: {task_data.get('client')}")
        print(f"Module: {task_data.get('module')}")
    else:
        print(f"Error fetching task: {task}")
        return
    
    # Add a method to post time
    def post_time(task_id, person_id, date, time_value, work_type_id, description=None, billable=False):
        """Post time to a task."""
        data = {
            "taskid": task_id,
            "personid": person_id,
            "date": date,
            "time": time_value,
            "worktypeid": work_type_id,
            "billable": "true" if billable else "false"
        }
        
        if description:
            data["description"] = description
            
        return api._make_request('post', '/time', data=data)
    
    # Test posting time
    today = datetime.now().strftime("%Y-%m-%d")
    time_value = "1.00"  # 1 hour in decimal format
    description = "Testing API time entry"
    
    print(f"\nPosting time to task {task_id}...")
    print(f"Date: {today}")
    print(f"Time: {time_value}")
    print(f"Work Type ID: {work_type_id}")
    print(f"Person ID: {person_id}")
    print(f"Description: {description}")
    print(f"Billable: False")
    
    # First, let's check if we can get time entries
    print("\nChecking if we can get time entries...")
    get_time_response = api.get_time(task_id=task_id)
    
    if get_time_response.get("status") == "OK":
        print("Successfully retrieved time entries.")
        time_count = get_time_response.get("listcount", 0)
        print(f"Found {time_count} existing time entries for this task.")
    else:
        print(f"Error getting time entries: {get_time_response}")
    
    # Now try to post time
    print("\nAttempting to post time...")
    post_time_response = post_time(
        task_id=task_id,
        person_id=person_id,
        date=today,
        time_value=time_value,
        work_type_id=work_type_id,
        description=description,
        billable=False
    )
    
    if post_time_response.get("status") == "OK":
        print("Successfully posted time!")
        print(f"Time Entry ID: {post_time_response.get('timeid')}")
        print("\nFull Response:")
        print(json.dumps(post_time_response, indent=2))
    else:
        print(f"Error posting time: {post_time_response}")
        print("\nFull Error Response:")
        print(json.dumps(post_time_response, indent=2))

if __name__ == "__main__":
    main() 