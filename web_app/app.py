"""
Flask web application for Intervals time entry management.
Provides user-friendly interface for posting time entries.
"""
import sys
import os
# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from core.intervals_api import IntervalsAPI
from core.config import get_api_key, get_default_task_id, get_default_work_type
from datetime import datetime
import webbrowser
from threading import Timer

app = Flask(__name__)
CORS(app)

# Global API instance
api = None
person_id = None

def init_api():
    """Initialize API connection and get person ID."""
    global api, person_id
    try:
        api_key = get_api_key()
        api = IntervalsAPI(api_key)

        # Get user info
        user_info = api.get_me()
        if user_info.get("status") == "OK":
            person_id = user_info['me'][0]['id']
            return True, f"Connected as {user_info['me'][0]['firstname']} {user_info['me'][0]['lastname']}"
        else:
            return False, f"API Error: {user_info}"
    except ValueError as e:
        return False, str(e)
    except Exception as e:
        return False, f"Connection error: {str(e)}"


@app.route('/')
def index():
    """Render main page."""
    success, message = init_api()
    if not success:
        return render_template('index.html', error=message)
    return render_template('index.html', user_message=message)


@app.route('/api/work-types', methods=['GET'])
def get_work_types():
    """Get all available work types."""
    try:
        if not api:
            init_api()

        # Get project work types (more accessible than /worktype)
        # Use high limit to get all available work types
        work_types_response = api._make_request('get', '/projectworktype', params={'limit': 1000})

        if work_types_response.get("status") == "OK":
            work_types_dict = {}

            # Collect unique work types by worktypeid
            for pwt in work_types_response.get("projectworktype", []):
                worktype_id = pwt.get('worktypeid')
                worktype_name = pwt.get('worktype', 'Unknown')

                if worktype_id and worktype_name and worktype_id not in work_types_dict:
                    work_types_dict[worktype_id] = {
                        'id': worktype_id,
                        'name': worktype_name
                    }

            # Convert to list and sort
            work_types = list(work_types_dict.values())
            work_types.sort(key=lambda x: x['name'])

            return jsonify({
                'success': True,
                'work_types': work_types
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to fetch work types'
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    """Get available tasks."""
    try:
        if not api:
            init_api()

        # Get tasks - filter for open tasks only
        tasks_response = api.get_tasks()

        if tasks_response.get("status") == "OK":
            tasks = []
            for task in tasks_response.get("task", []):
                # Only include open tasks (status = 'Open')
                if task.get('status') == 'Open':
                    tasks.append({
                        'id': task.get('id'),
                        'title': task.get('title', 'Unknown'),
                        'project': task.get('project', '')
                    })

            # Limit to 100 most recent open tasks
            tasks = tasks[:100]

            return jsonify({
                'success': True,
                'tasks': tasks
            })
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to fetch tasks'
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/post-time', methods=['POST'])
def post_time():
    """Post time entries."""
    try:
        if not api or not person_id:
            init_api()

        entries = request.json.get('entries', [])

        if not entries:
            return jsonify({
                'success': False,
                'error': 'No entries provided'
            }), 400

        results = []

        for entry in entries:
            # Prepare data
            data = {
                "taskid": entry['task_id'],
                "personid": person_id,
                "date": entry['date'],
                "time": entry['time'],
                "worktypeid": entry['work_type_id'],
                "billable": "true" if entry.get('billable', False) else "false"
            }

            if entry.get('description'):
                data["description"] = entry['description']

            # Post to API
            response = api._make_request('post', '/time', data=data)

            if response.get("status") == "Created" and response.get("code") == 201:
                time_entry = response.get("time", {})
                results.append({
                    'success': True,
                    'entry_id': time_entry.get('id'),
                    'date': time_entry.get('date'),
                    'time': time_entry.get('time'),
                    'description': entry.get('description', '')
                })
            else:
                results.append({
                    'success': False,
                    'error': response.get('error', 'Unknown error'),
                    'description': entry.get('description', '')
                })

        # Check if all succeeded
        all_success = all(r['success'] for r in results)

        return jsonify({
            'success': all_success,
            'results': results
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@app.route('/api/config', methods=['GET'])
def get_config():
    """Get default configuration."""
    return jsonify({
        'default_task_id': get_default_task_id(),
        'default_work_type': get_default_work_type(),
        'today': datetime.now().strftime('%Y-%m-%d')
    })


def open_browser():
    """Open browser after a short delay."""
    webbrowser.open('http://127.0.0.1:5000')


if __name__ == '__main__':
    print("\n" + "="*60)
    print("  Interval Cheat Code v0.1")
    print("  Credit: Rajesh Alda")
    print("="*60)
    print("\nStarting server...")
    print("Opening browser at http://127.0.0.1:5000")
    print("\nPress Ctrl+C to stop the server\n")

    # Open browser after 1 second
    Timer(1, open_browser).start()

    app.run(debug=True, use_reloader=False, port=5000)
