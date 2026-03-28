import os
import argparse
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ClaudeSyncHandler(FileSystemEventHandler):
    def __init__(self, directory, api_key):
        self.directory = directory
        self.api_key = api_key

    def on_modified(self, event):
        if event.is_directory:
            return
        self.sync_file_with_claude(event.src_path)

    def sync_file_with_claude(self, file_path):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
            response = requests.post(
                "https://api.claude.ai/sync",
                json={"file_name": os.path.basename(file_path), "content": content},
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            response.raise_for_status()

            if response.status_code == 200:
                remote_content = response.json().get("content")
                if remote_content is not None:
                    with open(file_path, 'w') as file:
                        file.write(remote_content)
                    print(f"Synced file: {file_path}")
                else:
                    print(f"No changes detected for file: {file_path}")
            else:
                print(f"Failed to sync file: {file_path}. Error: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Network error while syncing file {file_path}: {e}")
        except Exception as e:
            print(f"Error while syncing file {file_path}: {e}")

def main():
    parser = argparse.ArgumentParser(description="Claude Code Real-Time Sync")
    parser.add_argument("--dir", required=True, help="Path to the local directory to sync")
    parser.add_argument("--api-key", required=True, help="Claude API key")
    args = parser.parse_args()

    if not os.path.isdir(args.dir):
        print(f"Error: The directory {args.dir} does not exist.")
        return

    event_handler = ClaudeSyncHandler(args.dir, args.api_key)
    observer = Observer()
    observer.schedule(event_handler, path=args.dir, recursive=True)

    print(f"Starting Claude Code Real-Time Sync for directory: {args.dir}")
    try:
        observer.start()
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()
        print("Stopped Claude Code Real-Time Sync.")
    observer.join()

if __name__ == "__main__":
    main()
