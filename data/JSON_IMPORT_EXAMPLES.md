# JSON Import Format Examples

## Basic Format

The web app supports importing time entries from JSON. You can use defaults at the top level and override per entry.

## Getting Task IDs and Work Type IDs

**Before creating your JSON:**
- **Task IDs**: Use Postman to call `https://api.myintervals.com/task?limit=20000`
  - Headers: `Accept: application/json` and `Authorization: Basic <username:password>` (username = your API key, password = leave blank)
- **Work Type IDs**: See `all_worktypes.txt` in this folder - all work types with IDs are listed there

**Work Type Options:**
- You can use either `work_type_id` (numeric ID like "305064") OR `work_type` (friendly name like "India-Meeting")
- Using IDs is more reliable, but names are easier to read

---

## Example 1: Simple - All Same Task/Work Type

All entries use the same task and work type:

```json
{
  "task_id": "123456789",
  "work_type_id": "305064",
  "time": "8",
  "billable": false,
  "entries": [
    {
      "date": "2026-01-09",
      "description": "Daily standup meeting"
    },
    {
      "date": "2026-01-10",
      "description": "Team sync meeting"
    },
    {
      "date": "2026-01-11",
      "description": "Sprint planning"
    }
  ]
}
```

**Or using friendly name:**
```json
{
  "task_id": "123456789",
  "work_type": "India-Meeting",
  "time": "8",
  "billable": false,
  "entries": [
    {
      "date": "2026-01-09",
      "description": "Daily standup meeting"
    },
    {
      "date": "2026-01-10",
      "description": "Team sync meeting"
    }
  ]
}
```

---

## Example 2: Mixed Durations

Same task/work type, but different time for each entry:

```json
{
  "task_id": "123456789",
  "work_type_id": "304999",
  "entries": [
    {
      "date": "2026-01-09",
      "description": "Built authentication feature",
      "time": "4"
    },
    {
      "date": "2026-01-09",
      "description": "Code review",
      "time": "2"
    },
    {
      "date": "2026-01-09",
      "description": "Bug fixes",
      "time": "1.5"
    }
  ]
}
```

---

## Example 3: Different Work Types

Same task, but different work types per entry:

```json
{
  "task_id": "123456789",
  "time": "8",
  "entries": [
    {
      "date": "2026-01-09",
      "work_type_id": "304999",
      "description": "Feature development"
    },
    {
      "date": "2026-01-10",
      "work_type_id": "305064",
      "description": "Client call"
    },
    {
      "date": "2026-01-11",
      "work_type_id": "327235",
      "description": "API documentation"
    }
  ]
}
```

---

## Example 4: Completely Custom (Different Everything)

Each entry has its own task, work type, and duration:

```json
{
  "entries": [
    {
      "date": "2026-01-09",
      "task_id": "123456789",
      "work_type_id": "305064",
      "time": "2",
      "description": "Daily standup",
      "billable": false
    },
    {
      "date": "2026-01-09",
      "task_id": "123456789",
      "work_type_id": "304999",
      "time": "4",
      "description": "Feature X development",
      "billable": true
    },
    {
      "date": "2026-01-10",
      "task_id": "123456789",
      "work_type_id": "327235",
      "time": "3",
      "description": "Updated README",
      "billable": false
    },
    {
      "date": "2026-01-10",
      "task_id": "123456789",
      "work_type_id": "305065",
      "time": "1.5",
      "description": "Testing feature X",
      "billable": true
    }
  ]
}
```

---

## Example 5: Mixed (Defaults + Overrides)

Use defaults for common values, override when needed:

```json
{
  "task_id": "123456789",
  "work_type_id": "304999",
  "time": "8",
  "billable": false,
  "entries": [
    {
      "date": "2026-01-09",
      "description": "Regular development work"
    },
    {
      "date": "2026-01-10",
      "description": "More development",
      "time": "6"
    },
    {
      "date": "2026-01-10",
      "description": "Team meeting",
      "work_type_id": "305064",
      "time": "2"
    },
    {
      "date": "2026-01-11",
      "description": "Client project",
      "task_id": "987654321",
      "billable": true
    }
  ]
}
```

---

## Example 6: Full Week Schedule

Complete week with various activities:

```json
{
  "task_id": "123456789",
  "entries": [
    {
      "date": "2026-01-13",
      "work_type_id": "305064",
      "time": "1",
      "description": "Monday standup"
    },
    {
      "date": "2026-01-13",
      "work_type_id": "304999",
      "time": "7",
      "description": "Sprint work"
    },
    {
      "date": "2026-01-14",
      "work_type_id": "304999",
      "time": "6",
      "description": "Feature development"
    },
    {
      "date": "2026-01-14",
      "work_type_id": "305065",
      "time": "2",
      "description": "Testing"
    },
    {
      "date": "2026-01-15",
      "work_type_id": "305064",
      "time": "2",
      "description": "Sprint review"
    },
    {
      "date": "2026-01-15",
      "work_type_id": "327235",
      "time": "4",
      "description": "Updated docs"
    },
    {
      "date": "2026-01-15",
      "work_type_id": "304999",
      "time": "2",
      "description": "Bug fixes"
    }
  ]
}
```

---

## Field Reference

### Top-level (defaults applied to all entries)
- `task_id` - Default task ID
- `work_type` or `work_type_id` - Default work type (name or ID)
- `time` - Default duration in hours
- `billable` - Default billable status (true/false)

### Per-entry fields
- `date` - **Required** - Format: YYYY-MM-DD
- `description` - What you worked on
- `task_id` - Override default task
- `work_type` or `work_type_id` - Override default work type
- `time` - Override default duration (decimal hours: 1.5, 2.25, etc.)
- `billable` - Override default billable status

### Work Type Options
Common work types (use the name):
- `India-Meeting`
- `India-Engineering`
- `India-Design`
- `India-Documentation`
- `India-Quality Assurance`
- `India-Project Management`
- `India-Training`
- `India-Customer Support`
- `India-Troubleshooting`

You can also use work type IDs instead of names.

---

## Tips

1. **Minimal format** - If all entries share task/work type, put them at top level
2. **Per-entry override** - Override only what's different in each entry
3. **Decimal hours** - Use 0.25, 0.5, 0.75, 1.5, etc.
4. **Date format** - Always YYYY-MM-DD
5. **Work type** - Use friendly name (India-Meeting) or ID (123456)

---

## How to Use

1. Copy one of the examples above
2. Modify dates, descriptions, tasks, etc.
3. Click "Import JSON" button in the web app
4. Paste your JSON
5. Click "Import"
6. Review entries and submit!
