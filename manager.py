import json
import subprocess
import os
import time
import sys

CONFIG_FILE = "config.json"
STREAMER_SCRIPT = "streamer.py"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"Config file {CONFIG_FILE} not found.")
        return []
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def main():
    config = load_config()
    if not config:
        print("No configuration found or empty.")
        sys.exit(1)

    processes = []
    
    # Get absolute path of the directory
    base_dir = os.path.dirname(os.path.abspath(__file__))
    script_path = os.path.join(base_dir, STREAMER_SCRIPT)

    print(f"Starting {len(config)} streams...")

    for entry in config:
        uuid = entry.get('uuid')
        video_filename = entry.get('file')
        
        if not uuid or not video_filename:
            print(f"Skipping invalid entry: {entry}")
            continue

        video_path = os.path.join(base_dir, video_filename)
        if not os.path.exists(video_path):
            print(f"Warning: Video file not found: {video_path}")
            continue

        cmd = ["python3", script_path, video_path, uuid]
        print(f"Launching stream for {uuid} ({video_filename})...")
        
        # Spawn process
        p = subprocess.Popen(cmd)
        processes.append(p)

    print("All streams launched. Press Ctrl+C to stop.")

    try:
        while True:
            time.sleep(1)
            # Check if processes are alive (optional enhancement)
            for i, p in enumerate(processes):
                if p.poll() is not None:
                     print(f"Process {p.pid} ended unexpectedly. (Logic to restart could be added here)")
                     # For now, just logging.
    except KeyboardInterrupt:
        print("\nStopping all streams...")
        for p in processes:
            p.terminate()
        print("Done.")

if __name__ == "__main__":
    main()
