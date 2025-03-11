import requests
import json

class IntervalsAPI:
    def __init__(self, api_key):
        """Initialize the Intervals API client with the API key."""
        self.api_key = api_key
        self.base_url = "https://api.myintervals.com"
        # Use the API key as the username with an empty password
        self.auth = (api_key, "")
    
    def _make_request(self, method, endpoint, params=None, data=None):
        """Make a request to the Intervals API."""
        url = f"{self.base_url}{endpoint}"
        
        if method.lower() == 'get':
            response = requests.get(url, auth=self.auth, params=params)
        elif method.lower() == 'post':
            headers = {'Content-Type': 'application/json'}
            response = requests.post(url, auth=self.auth, json=data, headers=headers)
        elif method.lower() == 'put':
            headers = {'Content-Type': 'application/json'}
            response = requests.put(url, auth=self.auth, json=data, headers=headers)
        elif method.lower() == 'delete':
            response = requests.delete(url, auth=self.auth)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        return response.json()
    
    def get_me(self):
        """Get information about the authenticated user."""
        return self._make_request('get', '/me')
    
    def get_projects(self, active=True, limit=None):
        """Get a list of projects."""
        params = {'active': 'true' if active else 'false'}
        if limit:
            params['limit'] = limit
        return self._make_request('get', '/project', params=params)
    
    def get_tasks(self, project_id=None, limit=None):
        """Get a list of tasks, optionally filtered by project."""
        params = {}
        if project_id:
            params['projectid'] = project_id
        if limit:
            params['limit'] = limit
        return self._make_request('get', '/task', params=params)
    
    def get_task_by_id(self, task_id):
        """Get a specific task by its ID."""
        return self._make_request('get', f'/task/{task_id}/')
    
    def create_task(self, project_id, name, description=None, priority=None, 
                   estimate=None, person_id=None, status=None):
        """Create a new task."""
        data = {
            'projectid': project_id,
            'name': name
        }
        
        if description:
            data['description'] = description
        if priority:
            data['priority'] = priority
        if estimate:
            data['estimate'] = estimate
        if person_id:
            data['personid'] = person_id
        if status:
            data['status'] = status
            
        return self._make_request('post', '/task', data=data)
    
    def update_task(self, task_id, **kwargs):
        """Update an existing task."""
        return self._make_request('put', f'/task/{task_id}/', data=kwargs)
    
    def get_time(self, task_id=None, person_id=None, start_date=None, end_date=None):
        """Get time entries, optionally filtered by task, person, or date range."""
        params = {}
        if task_id:
            params['taskid'] = task_id
        if person_id:
            params['personid'] = person_id
        if start_date:
            params['datebegin'] = start_date
        if end_date:
            params['dateend'] = end_date
            
        return self._make_request('get', '/time', params=params)
    
    def create_time(self, task_id, person_id, date, time_value, work_type_id, description=None, billable=False):
        """Create a new time entry.
        
        Args:
            task_id (str): The ID of the task to log time against
            person_id (str): The ID of the person logging the time
            date (str): The date in YYYY-MM-DD format
            time_value (str): The time in decimal hours (e.g., "1.00" for 1 hour)
            work_type_id (str): The ID of the work type
            description (str, optional): Description of the work
            billable (bool, optional): Whether the time is billable
            
        Returns:
            dict: The API response
        """
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
            
        return self._make_request('post', '/time', data=data)
    
    def get_work_types(self, project_id=None):
        """Get a list of work types, optionally filtered by project."""
        params = {}
        if project_id:
            params['projectid'] = project_id
        return self._make_request('get', '/projectworktype', params=params)

if __name__ == "__main__":
    # Your API key
    api_key = "7ghfnbbbo6s"
    
    # Create an instance of the IntervalsAPI class
    api = IntervalsAPI(api_key)
    
    # Get user information
    try:
        user_info = api.get_me()
        
        if user_info.get("status") == "OK":
            print("Successfully connected to Intervals API!")
            print("\nUser Information:")
            me_data = user_info.get("me", [])[0]
            print(f"Name: {me_data.get('firstname')} {me_data.get('lastname')}")
            print(f"Title: {me_data.get('title')}")
            print(f"Username: {me_data.get('username')}")
            print(f"User ID: {me_data.get('id')}")
            print(f"Client: {me_data.get('client')}")
            print(f"User Group: {me_data.get('group')}")
            
            # Get a list of projects (limited to 5)
            print("\nFetching projects...")
            projects = api.get_projects(limit=5)
            if projects.get("status") == "OK":
                print(f"Found {projects.get('listcount')} projects")
                for project in projects.get("project", []):
                    print(f"- {project.get('name')} (ID: {project.get('id')})")
            else:
                print(f"Error fetching projects: {projects}")
            
            print("\nFull User Response:")
            print(json.dumps(user_info, indent=2))
        else:
            print(f"Error: {user_info}")
    except Exception as e:
        print(f"Exception occurred: {str(e)}") 