import os
import subprocess
import sys

res = subprocess.run(["netstat", "-ano"], capture_output=True, text=True)
pids = set()
for line in res.stdout.splitlines():
    if ":8080 " in line and "LISTENING" in line:
        parts = line.strip().split()
        pids.add(parts[-1])

print(f"Found PIDs on 8080: {pids}")
for pid in pids:
    try:
        subprocess.run(["taskkill", "/F", "/PID", pid], check=True)
        print(f"Killed PID {pid}")
    except Exception as e:
        print(f"Error killing PID {pid}: {e}")
