#!/usr/bin/env python
"""
Simple script to post time to the Meeting Tracker Internal Project task.
"""
import requests
import json
from datetime import datetime

def main():
    # Read the time entries from JSON file
    try:
        with open('time_entries.json', 'r') as f:
            time_entries = json.load(f)
    except FileNotFoundError:
        print("Error: time_entries.json file not found!")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON format in time_entries.json!")
        return
    
    # Fixed values
    API_KEY = "7ghfnbbbo6s"
    base_url = "https://api.myintervals.com"
    
    # Get user information to get person ID
    auth = (API_KEY, "")
    me_response = requests.get(f"{base_url}/me", auth=auth)
    me_data = me_response.json()
    
    if me_data.get("status") != "OK":
        print(f"Error connecting to Intervals API: {me_data}")
        return
    
    person_id = me_data['me'][0]['id']
    print(f"Connected as: {me_data['me'][0]['firstname']} {me_data['me'][0]['lastname']} (ID: {person_id})")
    
    # Process each entry
    for entry in time_entries['entries']:
        print(f"\nPosting time entry for {entry['date']}...")
        print(f"Description: {entry['description']}")
        print(f"Time: {time_entries['time']} hours")
        
        # Prepare data for posting time
        time_data = {
            "taskid": time_entries['task_id'],
            "personid": person_id,
            "date": entry['date'],
            "time": time_entries['time'],
            "worktypeid": time_entries['work_type_id'],
            "billable": "true" if time_entries['billable'] else "false",
            "description": entry['description']
        }
        
        # Post time
        headers = {'Content-Type': 'application/json'}
        time_response = requests.post(f"{base_url}/time", auth=auth, json=time_data, headers=headers)
        post_time_response = time_response.json()
        
        # Check for success (status code 201 means Created)
        if post_time_response.get("status") == "Created" and post_time_response.get("code") == 201:
            print("\nSUCCESS: Time entry created!")
            time_entry = post_time_response.get("time", {})
            print(f"Time Entry ID: {time_entry.get('id')}")
            print(f"Date: {time_entry.get('date')}")
            print(f"Time: {time_entry.get('time')} hours")
            print(f"Work Type: {time_entry.get('worktype')}")
        else:
            print(f"\nERROR: Failed to post time: {post_time_response}")
            print("Stopping further entries.")
            break

if __name__ == "__main__":
    main() 