#!/bin/bash
# Run daily_astro_telegram.py at 6:00 AM and 6:30 PM
source /workspaces/2026-astroquantdayplanner/.venv/bin/activate
cd /workspaces/2026-astroquantdayplanner
/workspaces/2026-astroquantdayplanner/.venv/bin/python daily_astro_telegram.py
