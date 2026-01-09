import sys
import os
# Add parent directory to path to import core module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.intervals_api import IntervalsAPI
from core.config import get_api_key
import json

def main():
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
    
    # Get all available work types (not project-specific)
    print("\n--- GLOBAL WORK TYPES ---")
    work_types = api._make_request('get', '/worktype')
    
    if work_types.get("status") == "OK":
        print(f"Found {work_types.get('listcount', 0)} global work types")
        
        # Print all work types
        for work_type in work_types.get("worktype", []):
            work_type_id = work_type.get("id")
            work_type_name = work_type.get("name", "")
            
            print(f"ID: {work_type_id}, Name: {work_type_name}")
    else:
        print(f"Error fetching global work types: {work_types}")
    
    # Get all project work types
    print("\n--- PROJECT WORK TYPES ---")
    project_work_types = api._make_request('get', '/projectworktype', params={'limit': 1000})
    
    if project_work_types.get("status") == "OK":
        print(f"Found {project_work_types.get('listcount', 0)} project work types")
        
        # Print all project work types
        for work_type in project_work_types.get("projectworktype", []):
            work_type_id = work_type.get("id")
            worktype_id = work_type.get("worktypeid")
            work_type_name = work_type.get("worktype", "")
            project_id = work_type.get("projectid")
            
            # Handle None values
            if work_type_name is None:
                work_type_name = ""
            
            print(f"ID: {work_type_id}, WorkType ID: {worktype_id}, Name: {work_type_name}, Project ID: {project_id}")
    else:
        print(f"Error fetching project work types: {project_work_types}")
    
    # Get task-specific work types
    task_id = "1234567980"  # Meeting Tracker Internal Project
    print(f"\n--- WORK TYPES FOR TASK {task_id} ---")
    task = api.get_task_by_id(task_id)
    
    if task.get("status") == "OK":
        project_id = task.get('task', {}).get('projectid')
        print(f"Task: {task.get('task', {}).get('title')}")
        print(f"Project ID: {project_id}")
        
        if project_id:
            task_work_types = api._make_request('get', '/projectworktype', params={'projectid': project_id, 'limit': 1000})
            
            if task_work_types.get("status") == "OK":
                print(f"Found {task_work_types.get('listcount', 0)} work types for this project")
                
                for work_type in task_work_types.get("projectworktype", []):
                    work_type_id = work_type.get("id")
                    worktype_id = work_type.get("worktypeid")
                    work_type_name = work_type.get("worktype", "")
                    
                    print(f"ID: {work_type_id}, WorkType ID: {worktype_id}, Name: {work_type_name}")
            else:
                print(f"Error fetching task work types: {task_work_types}")
    else:
        print(f"Error fetching task: {task}")

if __name__ == "__main__":
    main() 