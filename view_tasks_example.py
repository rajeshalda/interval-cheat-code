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
    
    # Get projects to select a project ID
    projects = api.get_projects()
    if projects.get("status") != "OK":
        print(f"Error fetching projects: {projects}")
        return
    
    print("\nAvailable Projects:")
    for i, project in enumerate(projects.get("project", [])):
        print(f"{i+1}. {project.get('name')} (ID: {project.get('id')})")
    
    # Get all tasks
    print("\nFetching all tasks...")
    tasks = api.get_tasks(limit=10)  # Limiting to 10 tasks for readability
    
    if tasks.get("status") == "OK":
        task_count = tasks.get("listcount", 0)
        print(f"Found {task_count} tasks in total")
        
        if task_count > 0:
            print("\nTasks (showing up to 10):")
            for task in tasks.get("task", []):
                task_id = task.get("id")
                task_local_id = task.get("localid")
                task_title = task.get("title")
                project_name = task.get("project")
                status = task.get("status")
                
                print(f"Task ID: {task_id} (Local ID: {task_local_id})")
                print(f"Title: {task_title}")
                print(f"Project: {project_name}")
                print(f"Status: {status}")
                print("-" * 50)
        else:
            print("No tasks found.")
    else:
        print(f"Error fetching tasks: {tasks}")
    
    # Try to get tasks for a specific project
    if projects.get("project"):
        selected_project = projects["project"][0]
        project_id = selected_project["id"]
        project_name = selected_project["name"]
        
        print(f"\nFetching tasks for project: {project_name} (ID: {project_id})...")
        project_tasks = api.get_tasks(project_id=project_id, limit=5)
        
        if project_tasks.get("status") == "OK":
            task_count = project_tasks.get("listcount", 0)
            print(f"Found {task_count} tasks in project '{project_name}'")
            
            if task_count > 0:
                print("\nProject Tasks (showing up to 5):")
                for task in project_tasks.get("task", []):
                    task_id = task.get("id")
                    task_local_id = task.get("localid")
                    task_title = task.get("title")
                    status = task.get("status")
                    
                    print(f"Task ID: {task_id} (Local ID: {task_local_id})")
                    print(f"Title: {task_title}")
                    print(f"Status: {status}")
                    print("-" * 50)
            else:
                print(f"No tasks found in project '{project_name}'.")
        else:
            print(f"Error fetching tasks for project: {project_tasks}")

if __name__ == "__main__":
    main() 