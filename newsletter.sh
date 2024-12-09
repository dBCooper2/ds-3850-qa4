#!/bin/bash

# TO RUN THIS FILE WITH cron:
#  - Make sure the script is executable:
#    - chmod +x /Users/dB/Desktop/fall_24/DS-3850/friday-projects/quarterly-assessment-4/newsletter.sh
#    - MAYBE use chmod 777 shell_script.sh and chmod 777 app.py to ensure that the cron job can run it
#  - Set up the cron job:
#    - crontab -e
#    - Set a line to run at the time you want:
#      - 0 6 * * * This is 6:00AM, every day
#
# To Change the Time on the cron job:
# * * * * * command_to_execute
# │ │ │ │ │
# │ │ │ │ └─── Day of the week (0 - 7) (Sunday = 0 or 7)
# │ │ │ └──── Month (1 - 12)
# │ │ └───── Day of the month (1 - 31)
# │ └────── Hour (0 - 23)
# └─────── Minute (0 - 59)

# What is going on?
# The cron job schedules this shell script to run at the specified time and date
# This script creates a file to record logs from the app in the event an error occurs (the cron job will not log anything by default)
# The script takes in a project directory and a path to the virtual environment within the project
# After checking that the venv exists, the script starts the venv, runs the app, and exits after logging an exit code to the log file.
# Statuses are 0 if the run was successful, and any other number if the app failed to run, with the number indicating an error.


# Logging
LOGFILE="/Users/dB/Desktop/fall_24/DS-3850/friday-projects/quarterly-assessment-4/newsletter.log"

# Project and virtual environment paths
PROJECT_DIR="/Users/dB/Desktop/fall_24/DS-3850/friday-projects/quarterly-assessment-4"
VENV_PATH="${PROJECT_DIR}/.venv/bin/activate"

# Timestamp for logging
echo "Newsletter run started at $(date)" >> "$LOGFILE"

# Check if virtual environment exists
if [ ! -f "$VENV_PATH" ]; then
    echo "Virtual environment not found!" >> "$LOGFILE"
    exit 1
fi

# Activate virtual environment
source "$VENV_PATH"

# Change to project directory
cd "$PROJECT_DIR"

# Run the script with error handling
python3 app.py >> "$LOGFILE" 2>&1

# Capture the exit status
STATUS=$?

# Deactivate virtual environment
deactivate

# Log the result
if [ $STATUS -eq 0 ]; then
    echo "Newsletter run completed successfully at $(date)\n" >> "$LOGFILE"
else
    echo "Newsletter run failed with status $STATUS at $(date)\n" >> "$LOGFILE"
fi