from intervals_api import IntervalsAPI
import json
from datetime import datetime
import argparse

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Post time to an Intervals task')
    parser.add_argument('--task-id', type=str, default="16474442", help='Task ID (default: 16474442 - Meeting Tracker Internal Project)')
    parser.add_argument('--time', type=str, default="1.00", help='Time in decimal hours (default: 1.00)')
    parser.add_argument('--date', type=str, default=datetime.now().strftime("%Y-%m-%d"), help='Date in YYYY-MM-DD format (default: today)')
    parser.add_argument('--description', type=str, default="", help='Description of work (default: empty)')
    parser.add_argument('--billable', action='store_true', help='Mark time as billable (default: false)')
    args = parser.parse_args()
    
    # Your API key
    api_key = "7ghfnbbbo6s"
    
    # Create an instance of the IntervalsAPI class
    api = IntervalsAPI(api_key)
    
    # Get user information to verify connection
    user_info = api.get_me()
    if user_info.get("status") != "OK":
        print(f"Error connecting to Intervals API: {user_info}")
        return
    
    person_id = user_info['me'][0]['id']
    print(f"Connected as: {user_info['me'][0]['firstname']} {user_info['me'][0]['lastname']} (ID: {person_id})")
    
    # Get the task details to confirm
    print(f"\nFetching task with ID: {args.task_id}...")
    task = api.get_task_by_id(args.task_id)
    
    if task.get("status") == "OK":
        task_data = task.get("task", {})
        print(f"Task: {task_data.get('title')}")
        print(f"Project: {task_data.get('project')}")
        print(f"Client: {task_data.get('client')}")
        print(f"Module: {task_data.get('module')}")
        
        # Get the project ID for this task
        project_id = task_data.get('projectid')
        
        # Get work types for this project
        def get_work_types(project_id=None):
            """Get a list of work types, optionally filtered by project."""
            params = {}
            if project_id:
                params['projectid'] = project_id
            return api._make_request('get', '/projectworktype', params=params)
        
        print(f"\nFetching work types for project ID: {project_id}...")
        project_work_types = get_work_types(project_id)
        
        if project_work_types.get("status") == "OK":
            # Find the India-Meeting work type
            india_meeting_id = None
            for work_type in project_work_types.get("projectworktype", []):
                work_type_name = work_type.get("worktype", "")
                if work_type_name and "india-meeting" in work_type_name.lower():
                    india_meeting_id = work_type.get("worktypeid")
                    print(f"Found India-Meeting work type! ID: {india_meeting_id}")
                    break
            
            if not india_meeting_id:
                print("Couldn't find India-Meeting work type. Using default work type ID.")
                india_meeting_id = "305064"  # Default India-Meeting ID
            
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
            
            # Post time
            print(f"\nPosting time to task {args.task_id}...")
            print(f"Date: {args.date}")
            print(f"Time: {args.time}")
            print(f"Work Type: India-Meeting (ID: {india_meeting_id})")
            print(f"Description: {args.description}")
            print(f"Billable: {args.billable}")
            
            post_time_response = post_time(
                task_id=args.task_id,
                person_id=person_id,
                date=args.date,
                time_value=args.time,
                work_type_id=india_meeting_id,
                description=args.description,
                billable=args.billable
            )
            
            # Check for success (status code 201 means Created)
            if post_time_response.get("status") == "Created" and post_time_response.get("code") == 201:
                print("\n✅ Successfully posted time!")
                time_entry = post_time_response.get("time", {})
                print(f"Time Entry ID: {time_entry.get('id')}")
                print(f"Date: {time_entry.get('date')}")
                print(f"Time: {time_entry.get('time')} hours")
                print(f"Work Type: {time_entry.get('worktype')}")
                print(f"Description: {time_entry.get('description')}")
                print(f"Billable: {time_entry.get('billable') == 't'}")
            else:
                print(f"\n❌ Error posting time: {post_time_response}")
        else:
            print(f"Error fetching work types: {project_work_types}")
    else:
        print(f"Error fetching task: {task}")

if __name__ == "__main__":
    main() 