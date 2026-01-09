# Quick Start Guide

Get up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Set Up Your API Key

```bash
# Copy the example file
cp .env.example .env

# Edit .env and add your API key
# Get your key from: https://www.myintervals.com/api/
```

**Edit `.env`:**
```env
INTERVALS_API_KEY=your_actual_api_key_here
```

## Step 3: Run the Web App

```bash
python web_app/app.py
```

The browser will open automatically!

## Alternative: Command Line Usage

**Post a time entry:**
```bash
python cli_tools/post_time.py --time 4 --description "Built feature X"
```

**Find work types:**
```bash
python cli_tools/find_worktype.py
```

## Need Help?

See [docs/SETUP.md](docs/SETUP.md) for detailed instructions.

## Security Note

✅ Never commit your `.env` file to Git!
✅ It's already in `.gitignore` so you're safe.
