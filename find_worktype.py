from intervals_api import IntervalsAPI
import json

def main():
    # Your API key
    api_key = "7ghfnbbbo6s"
    
    # Create an instance of the IntervalsAPI class
    api = IntervalsAPI(api_key)
    
    # Get user information to verify connection
    user_info = api.get_me()
    if user_info.get("status") != "OK":
        print(f"Error connecting to Intervals API: {user_info}")
        return
    
    print(f"Connected as: {user_info['me'][0]['firstname']} {user_info['me'][0]['lastname']}")
    
    # Add a method to get work types
    def get_work_types(project_id=None):
        """Get a list of work types, optionally filtered by project."""
        params = {}
        if project_id:
            params['projectid'] = project_id
        return api._make_request('get', '/projectworktype', params=params)
    
    # Get all work types
    print("\nFetching all work types...")
    work_types = get_work_types()
    
    if work_types.get("status") == "OK":
        print(f"Found {work_types.get('listcount', 0)} work types")
        
        # Print all work types to find India-Meeting
        print("\nAll Work Types:")
        india_meeting_id = None
        
        for work_type in work_types.get("projectworktype", []):
            work_type_id = work_type.get("id")
            worktype_id = work_type.get("worktypeid")
            work_type_name = work_type.get("worktype", "")
            project_id = work_type.get("projectid")
            
            # Handle None values
            if work_type_name is None:
                work_type_name = ""
            
            print(f"ID: {work_type_id}, WorkType ID: {worktype_id}, Name: {work_type_name}, Project ID: {project_id}")
            
            # Check if this is the India-Meeting work type
            if "india-meeting" in work_type_name.lower() or "india meeting" in work_type_name.lower():
                india_meeting_id = worktype_id  # Use the worktype ID, not the projectworktype ID
                print(f"\n*** Found India-Meeting work type! ID: {india_meeting_id}, ProjectWorkType ID: {work_type_id} ***")
        
        # If we didn't find it by name, let the user check the full list
        if not india_meeting_id:
            print("\nCouldn't find a work type with 'India-Meeting' in the name.")
            print("Please check the list above for the correct work type.")
            
            # Let's check if there's a Meeting work type
            print("\nChecking for any work type containing 'Meeting':")
            for work_type in work_types.get("projectworktype", []):
                work_type_name = work_type.get("worktype", "")
                if work_type_name and "meeting" in work_type_name.lower():
                    worktype_id = work_type.get("worktypeid")
                    project_id = work_type.get("projectid")
                    print(f"Found: ID: {work_type.get('id')}, WorkType ID: {worktype_id}, Name: {work_type_name}, Project ID: {project_id}")
    else:
        print(f"Error fetching work types: {work_types}")
    
    # Now let's check if we can get the specific task
    task_id = "16474442"  # Meeting Tracker Internal Project
    print(f"\nFetching task with ID: {task_id}...")
    task = api.get_task_by_id(task_id)
    
    if task.get("status") == "OK":
        print(f"Successfully retrieved task: {task.get('task', {}).get('title')}")
        
        # Get the project ID for this task
        project_id = task.get('task', {}).get('projectid')
        if project_id:
            print(f"\nFetching work types for project ID: {project_id}...")
            project_work_types = get_work_types(project_id)
            
            if project_work_types.get("status") == "OK":
                print(f"Found {project_work_types.get('listcount', 0)} work types for this project")
                
                print("\nProject Work Types:")
                for work_type in project_work_types.get("projectworktype", []):
                    work_type_id = work_type.get("id")
                    worktype_id = work_type.get("worktypeid")
                    work_type_name = work_type.get("worktype", "")
                    
                    print(f"ID: {work_type_id}, WorkType ID: {worktype_id}, Name: {work_type_name}")
            else:
                print(f"Error fetching project work types: {project_work_types}")
    else:
        print(f"Error fetching task: {task}")

if __name__ == "__main__":
    main() 