#!/usr/bin/env python3
import os
import shutil
import subprocess
from datetime import datetime, timedelta

# --- Configuration ---
MONITOR_PATH = os.path.expanduser("~/FIELD")
THRESHOLD_PERCENT = 80
CLEANUP_DIRS = {
    "logs": {"days": 30},
    "__pycache__": {"days": 7},
}
NOTIFICATION_TITLE = "Disk Space Alert"

def get_disk_usage(path):
    """Returns the disk usage of the specified path in percent."""
    total, used, free = shutil.disk_usage(path)
    return (used / total) * 100

def send_notification(message):
    """Sends a macOS notification."""
    subprocess.run([
        "osascript",
        "-e",
        f'display notification "{message}" with title "{NOTIFICATION_TITLE}"'
    ])

def cleanup_files(path, days):
    """Deletes files older than a specified number of days."""
    now = datetime.now()
    cutoff = now - timedelta(days=days)
    for root, _, files in os.walk(path):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                if os.path.getmtime(file_path) < cutoff.timestamp():
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
            except OSError as e:
                print(f"Error deleting {file_path}: {e}")

def main():
    """Main function to monitor disk space and perform cleanup."""
    usage = get_disk_usage(MONITOR_PATH)
    print(f"Current disk usage at {MONITOR_PATH}: {usage:.2f}%")

    if usage > THRESHOLD_PERCENT:
        message = f"Disk usage at {MONITOR_PATH} is {usage:.2f}%, exceeding the {THRESHOLD_PERCENT}% threshold."
        send_notification(message)
        
        for dir_name, config in CLEANUP_DIRS.items():
            path_to_clean = os.path.join(MONITOR_PATH, dir_name)
            if os.path.exists(path_to_clean):
                print(f"Cleaning up {path_to_clean}...")
                cleanup_files(path_to_clean, config["days"])

if __name__ == "__main__":
    main()

