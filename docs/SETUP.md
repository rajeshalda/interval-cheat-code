# Setup Guide

This guide will help you set up the Intervals Time Tracking System on your machine.

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- An Intervals account with API access

## Installation Steps

### 1. Install Python Dependencies

Navigate to the project root directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- `requests` - For API communication
- `Flask` - For the web application
- `Flask-CORS` - For cross-origin requests
- `python-dotenv` - For environment variable management

### 2. Set Up Your API Key

#### Step 2.1: Get Your API Key

1. Log in to your Intervals account
2. Go to [https://www.myintervals.com/api/](https://www.myintervals.com/api/)
3. Copy your API key (it will look something like: `7eeez9mbys6`)

#### Step 2.2: Create Your .env File

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

   **On Windows:**
   ```bash
   copy .env.example .env
   ```

2. Edit the `.env` file and add your actual API key:
   ```bash
   # Open in your favorite text editor
   notepad .env        # Windows
   nano .env           # Linux/Mac
   code .env           # VS Code
   ```

3. Replace `your_api_key_here` with your actual API key:
   ```env
   INTERVALS_API_KEY=7eeez9mbys6
   ```

#### Step 2.3: Configure Default Values (Optional)

You can also set default values in your `.env` file:

```env
# Your Intervals API key (REQUIRED)
INTERVALS_API_KEY=your_actual_api_key_here

# Optional: Default task ID
DEFAULT_TASK_ID=12345678

# Optional: Default project ID
DEFAULT_PROJECT_ID=959242

# Optional: Default work type (friendly name or ID)
DEFAULT_WORK_TYPE=India-Meeting
```

### 3. Verify Your Setup

Test that everything is configured correctly:

```bash
python cli_tools/find_worktype.py
```

If setup is correct, you should see:
```
Connected as: Your Name
--- GLOBAL WORK TYPES ---
Found X global work types
...
```

If you see an error like:
```
Error: INTERVALS_API_KEY not set!
```

Then your `.env` file is not configured correctly. Go back to Step 2.

## Security Best Practices

### Never Commit Your API Key!

- ✅ **DO:** Keep your API key in the `.env` file
- ✅ **DO:** Share `.env.example` with your team
- ❌ **DON'T:** Commit the `.env` file to Git
- ❌ **DON'T:** Hard-code API keys in Python files
- ❌ **DON'T:** Share your `.env` file via email/Slack

The `.gitignore` file is already configured to exclude `.env` from version control.

### File Permissions (Linux/Mac)

Restrict access to your `.env` file:

```bash
chmod 600 .env
```

This ensures only you can read the file.

## Using the System

### Option 1: Web Application (Easiest)

```bash
python web_app/app.py
```

Your browser will automatically open to the web interface.

### Option 2: Command Line

**Post individual time entry:**
```bash
python cli_tools/post_time.py --task-id 12345678 --time 4 --date 2026-01-09 --description "Built feature"
```

**Batch post from JSON:**
```bash
python cli_tools/post_meeting_time.py
```

**Find work types:**
```bash
python cli_tools/find_worktype.py
```

## Troubleshooting

### Error: "INTERVALS_API_KEY not set!"

**Cause:** The `.env` file doesn't exist or the API key is not set.

**Solution:**
1. Make sure you created the `.env` file (not `.env.example`)
2. Open `.env` and verify `INTERVALS_API_KEY=your_actual_key`
3. Make sure there are no spaces around the `=` sign
4. Make sure the API key doesn't have quotes around it

**Correct:**
```env
INTERVALS_API_KEY=7eeez9mbys6
```

**Incorrect:**
```env
INTERVALS_API_KEY = 7eeez9mbys6        # Has spaces
INTERVALS_API_KEY="7eeez9mbys6"        # Has quotes
INTERVALS_API_KEY=your_api_key_here    # Still has placeholder
```

### Error: "Unauthorized" or "User bad auth"

**Cause:** The API key is invalid or expired.

**Solution:**
1. Log in to Intervals
2. Go to [https://www.myintervals.com/api/](https://www.myintervals.com/api/)
3. Generate a new API key if needed
4. Update your `.env` file with the new key

### Error: "ModuleNotFoundError: No module named 'dotenv'"

**Cause:** Dependencies not installed.

**Solution:**
```bash
pip install -r requirements.txt
```

### Web App Not Opening

**Cause:** Flask not installed or port conflict.

**Solution:**
```bash
# Install Flask
pip install Flask Flask-CORS

# Try a different port
python web_app/app.py --port 5001
```

## Next Steps

- See [README_TIME_TRACKING.md](README_TIME_TRACKING.md) for usage guide
- Check out example scripts in `cli_tools/`
- Customize default values in `.env` file

## Getting Help

If you encounter issues:
1. Check this troubleshooting section
2. Verify your `.env` file is configured correctly
3. Check that dependencies are installed
4. Review error messages carefully

For API documentation, see: [intervals api endpoint.txt](intervals%20api%20endpoint.txt)
