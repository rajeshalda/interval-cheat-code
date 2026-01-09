import sys
import os
# Add parent directory to path to import core module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.intervals_api import IntervalsAPI
from core.config import get_api_key, get_default_task_id
import json

def main():
    # Check if a task ID was provided as a command-line argument
    if len(sys.argv) > 1:
        task_id = sys.argv[1]
    else:
        # If no task ID was provided, use one from the previous example
        task_id = get_default_task_id()

    # Get API key from environment
    try:
        api_key = get_api_key()
    except ValueError as e:
        print(f"Error: {e}")
        return
    
    # Create an instance of the IntervalsAPI class
    api = IntervalsAPI(api_key)
    
    # Get user information to verify connection
    user_info = api.get_me()
    if user_info.get("status") != "OK":
        print(f"Error connecting to Intervals API: {user_info}")
        return
    
    print(f"Connected as: {user_info['me'][0]['firstname']} {user_info['me'][0]['lastname']}")
    
    # Get the specific task by ID
    print(f"\nFetching task with ID: {task_id}...")
    task = api.get_task_by_id(task_id)
    
    if task.get("status") == "OK":
        # The response format for a single task has the task data directly in the "task" field
        task_data = task.get("task")
        
        if task_data:
            print("\nTask Details:")
            print(f"Task ID: {task_data.get('id')}")
            print(f"Local ID: {task_data.get('localid')}")
            print(f"Title: {task_data.get('title')}")
            print(f"Project: {task_data.get('project')}")
            print(f"Status: {task_data.get('status')}")
            print(f"Priority: {task_data.get('priority')}")
            
            # Check if the task has a description/summary
            summary = task_data.get('summary')
            if summary:
                print(f"Summary: {summary}")
            
            # Check if the task has assignees
            assignees = task_data.get('assignee')
            if assignees and isinstance(assignees, list):
                print("\nAssigned to:")
                for assignee in assignees:
                    print(f"- {assignee.get('assignee')} (ID: {assignee.get('personid')})")
            
            # Check if the task has owners
            owners = task_data.get('owner')
            if owners and isinstance(owners, list):
                print("\nOwned by:")
                for owner in owners:
                    print(f"- {owner.get('owner')} (ID: {owner.get('personid')})")
            
            # Check if the task has a due date
            due_date = task_data.get('datedue')
            if due_date:
                print(f"\nDue Date: {due_date}")
            
            # Check if the task has a module
            module = task_data.get('module')
            if module:
                print(f"Module: {module}")
            
            # Check if the task has an estimate
            estimate = task_data.get('estimate')
            if estimate:
                print(f"Estimate: {estimate} hours")
            
            # Check if the task has a creation date
            date_created = task_data.get('datecreated')
            if date_created:
                print(f"Created on: {date_created}")
            
            # Check if the task has an open date
            date_open = task_data.get('dateopen')
            if date_open:
                print(f"Opened on: {date_open}")
        else:
            print(f"No task found with ID: {task_id}")
    else:
        print(f"Error fetching task: {task}")

if __name__ == "__main__":
    main() 