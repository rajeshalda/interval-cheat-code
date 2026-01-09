# Interval Cheat Code

A modern, user-friendly web application for managing time entries in the Intervals time tracking platform.

**Version:** 0.1
**Credit:** Rajesh Alda

## Features

✅ **Easy to use** - Modern web interface, no command line needed
✅ **Multiple entries** - Add many time entries at once
✅ **Smart dropdowns** - Select tasks and work types from dropdown (no ID lookup!)
✅ **Flexible durations** - Different time for each entry
✅ **Date picker** - Easy date selection
✅ **Preview before submit** - Review all entries before posting
✅ **JSON import** - Import from existing JSON files
✅ **Real-time feedback** - See success/error for each entry

---

## Quick Setup (3 Steps)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

This installs Flask, Flask-CORS, requests, and python-dotenv.

### 2. Configure API Key

Create a `.env` file in the project root:

```bash
# Linux/Mac
cp .env.example .env

# Windows
copy .env.example .env
```

Edit `.env` and add your API key:

```env
INTERVALS_API_KEY=your_actual_api_key_here
```

Get your API key from: https://www.myintervals.com/api/

### 3. Run the Web App

```bash
python web_app/app.py
```

Browser will open automatically at http://127.0.0.1:5000

---

## Using the Web App

### Adding Time Entries

1. Click **"+ Add Entry"** to add a new entry form
2. Fill in:
   - **Date** - Pick from calendar
   - **Work Type** - Select from dropdown (e.g., India-Engineering, India-Meeting)
   - **Duration** - Hours in decimal (1.5, 2.25, 8, etc.)
   - **Task** - Select from dropdown (shows open tasks only)
   - **Description** - What you worked on
   - **Billable** - Check if billable
3. Add more entries as needed
4. Click **"Preview"** to review
5. Click **"Submit All Entries"**

### Importing from JSON

Click **"Import JSON"** and paste your JSON data. Supports multiple formats:

**Getting Task IDs and Work Type IDs:**
- **Task IDs**: Use Postman to call `https://api.myintervals.com/task?limit=20000`
  - Headers: `Accept: application/json` and `Authorization: Basic <username:password>` (username = your API key, password = leave blank)
- **Work Type IDs**: See `data/all_worktypes.txt` in the project - all work types with IDs are listed there

#### Format 1: Simple (All Same Task/Work Type)

```json
{
  "task_id": "12345678",
  "work_type_id": "305064",
  "time": "8",
  "entries": [
    {"date": "2026-01-09", "description": "Daily standup"},
    {"date": "2026-01-10", "description": "Team sync"}
  ]
}
```

Or use friendly name instead of ID:
```json
{
  "task_id": "12345678",
  "work_type": "India-Meeting",
  "time": "8",
  "entries": [
    {"date": "2026-01-09", "description": "Daily standup"},
    {"date": "2026-01-10", "description": "Team sync"}
  ]
}
```

#### Format 2: Mixed Durations

```json
{
  "task_id": "12345678",
  "work_type_id": "304999",
  "entries": [
    {"date": "2026-01-09", "description": "Feature A", "time": "4"},
    {"date": "2026-01-09", "description": "Bug fix", "time": "2"},
    {"date": "2026-01-10", "description": "Code review", "time": "1.5"}
  ]
}
```

#### Format 3: Different Work Types

```json
{
  "task_id": "12345678",
  "entries": [
    {
      "date": "2026-01-09",
      "work_type_id": "304999",
      "time": "6",
      "description": "Development"
    },
    {
      "date": "2026-01-09",
      "work_type_id": "305064",
      "time": "2",
      "description": "Client call"
    }
  ]
}
```

#### Format 4: Completely Custom (Different Everything)

```json
{
  "entries": [
    {
      "date": "2026-01-09",
      "task_id": "12345678",
      "work_type_id": "305064",
      "time": "2",
      "description": "Standup",
      "billable": false
    },
    {
      "date": "2026-01-09",
      "task_id": "12345678",
      "work_type_id": "304999",
      "time": "4",
      "description": "Feature X",
      "billable": true
    },
    {
      "date": "2026-01-10",
      "task_id": "12345678",
      "work_type_id": "327235",
      "time": "3",
      "description": "Updated README"
    }
  ]
}
```

#### Format 5: Defaults + Overrides

```json
{
  "task_id": "12345678",
  "work_type_id": "304999",
  "time": "8",
  "entries": [
    {
      "date": "2026-01-09",
      "description": "Regular dev work"
    },
    {
      "date": "2026-01-10",
      "description": "More dev",
      "time": "6"
    },
    {
      "date": "2026-01-10",
      "description": "Meeting",
      "work_type_id": "305064",
      "time": "2"
    }
  ]
}
```

### JSON Field Reference

**Top-level defaults** (applied to all entries unless overridden):
- `task_id` - Default task ID
- `work_type` or `work_type_id` - Default work type
- `time` - Default duration in hours
- `billable` - Default billable status (true/false)

**Per-entry fields**:
- `date` - **Required** - Format: YYYY-MM-DD
- `description` - What you worked on
- `task_id` - Override default task
- `work_type` or `work_type_id` - Override work type
- `time` - Override duration (decimal: 1.5, 2.25, etc.)
- `billable` - Override billable status

### Common Work Types

- India-Meeting
- India-Engineering / Development
- India-Design
- India-Documentation
- India-Quality Assurance
- India-Project Management
- India-Training
- India-Customer Support
- India-Troubleshooting

You can use the work type name or ID.

---

## Project Structure

```
interval-cheat/
├── web_app/                # Web application
│   ├── app.py             # Flask backend
│   ├── static/
│   │   ├── css/           # Styles
│   │   └── js/            # Frontend logic
│   └── templates/         # HTML
│
├── core/                   # API wrapper
│   ├── intervals_api.py
│   └── config.py          # Environment config
│
├── cli_tools/             # Command-line tools (optional)
├── data/                  # Sample data & examples
│   └── JSON_IMPORT_EXAMPLES.md
└── docs/                  # Documentation
```

---

## Environment Configuration

The `.env` file supports these settings:

```env
# Required
INTERVALS_API_KEY=your_api_key_here

# Optional defaults
DEFAULT_TASK_ID=12345678
DEFAULT_PROJECT_ID=959242
DEFAULT_WORK_TYPE=India-Meeting
```

---

## Command Line Tools (Optional)

If you prefer command line:

**Post single entry:**
```bash
python cli_tools/post_time.py --task-id 12345678 --time 4 --description "Work done"
```

**Batch post from JSON:**
```bash
python cli_tools/post_meeting_time.py
```

**Find work types:**
```bash
python cli_tools/find_worktype.py
```

---

## Troubleshooting

**"INTERVALS_API_KEY not set"**
- Make sure you created `.env` file (not `.env.example`)
- Check that `INTERVALS_API_KEY=` has your actual key
- No quotes needed around the key

**"Failed to load work types"**
- Check your API key has correct permissions
- Verify you can access https://www.myintervals.com

**Server won't start**
- Run `pip install -r requirements.txt` again
- Check if port 5000 is already in use

---

## Security

✅ API keys stored in `.env` file (never committed to Git)
✅ `.gitignore` already configured
✅ No hardcoded credentials in code

---

## More Examples

See `data/JSON_IMPORT_EXAMPLES.md` for 6 detailed JSON examples.

---

## Support

For detailed setup: `docs/SETUP.md`
For API reference: `docs/intervals api endpoint.txt`

---

## License

See [LICENSE](LICENSE) file for details.
