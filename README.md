# Time Entry Automation Tool

This tool automates the process of posting time entries to Intervals for the Meeting Tracker Internal Project.

## Setup Instructions

1. **Python Installation**
   - Make sure you have Python installed on your system
   - Required version: Python 3.6 or higher
   - You can download Python from: https://www.python.org/downloads/

2. **Install Required Packages**
   ```bash
   pip install requests
   ```

3. **Files Required**
   - `post_meeting_time.py` - The main script
   - `time_entries.json` - Contains the time entries data

4. **File Structure**
   ```
   your-folder/
   ├── post_meeting_time.py
   ├── time_entries.json
   └── README.md
   ```

## Usage

1. **Prepare the JSON File**
   - The `time_entries.json` file should contain your time entries
   - Structure:
   ```json
   {
       "task_id": "16474442",
       "work_type_id": "305064",
       "time": "8",
       "billable": false,
       "entries": [
           {
               "date": "2025-01-01",
               "description": "Your description here"
           }
       ]
   }
   ```

2. **Run the Script**
   ```bash
   python post_meeting_time.py
   ```
   - The script will process all entries in the JSON file
   - It will post each entry to Intervals
   - If any entry fails, the script will stop

3. **Output**
   - For each entry, you'll see:
     - Success/Error message
     - Time Entry ID
     - Date
     - Time posted
     - Work Type

## Important Notes

- The script uses a predefined API key
- Task ID 16474442 is for "Meeting Tracker Internal Project"
- Work Type ID 305064 is for "India-Meeting"
- Each entry will be posted with 8 hours
- Dates should be in YYYY-MM-DD format
- The script will stop if any entry fails to post

## Troubleshooting

If you encounter issues:
1. Check your internet connection
2. Verify the JSON file format is correct
3. Ensure all dates are in the correct format
4. Make sure the description field isn't empty

## Support

For any issues or questions, please contact the team lead. 