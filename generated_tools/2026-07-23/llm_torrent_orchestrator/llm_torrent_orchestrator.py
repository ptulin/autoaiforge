import os
import argparse
from tqdm import tqdm
from unittest.mock import MagicMock

class MockLibTorrent:
    """Mock implementation of libtorrent for testing."""
    class file_storage:
        pass

    @staticmethod
    def add_files(fs, file_path):
        pass

    class create_torrent:
        def __init__(self, fs):
            self.fs = fs

        def add_tracker(self, tracker):
            pass

        def set_creator(self, creator):
            pass

        def generate(self):
            return b"mock_torrent_data"

    @staticmethod
    def bencode(data):
        return data

    class session:
        def __init__(self):
            self.torrents = []

        def listen_on(self, start, end):
            pass

        def add_torrent(self, params):
            handle = MagicMock()
            handle.is_seed.side_effect = [False, False, True]
            self.torrents.append(handle)
            return handle

    class torrent_info:
        def __init__(self, torrent_file):
            self.torrent_file = torrent_file

        def name(self):
            return "mock_file_name"

    class storage_mode_t:
        storage_mode_sparse = "mock_storage_mode_sparse"

    @staticmethod
    def sleep(seconds):
        pass

lt = MockLibTorrent()

def create_torrent(file_path, trackers):
    """Creates a torrent file for the given file path."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    fs = lt.file_storage()
    lt.add_files(fs, file_path)

    t = lt.create_torrent(fs)

    for tracker in trackers:
        t.add_tracker(tracker)

    t.set_creator("LLM Torrent Orchestrator")

    torrent_file = os.path.splitext(file_path)[0] + ".torrent"
    with open(torrent_file, "wb") as f:
        f.write(lt.bencode(t.generate()))

    return torrent_file

def download_torrent(torrent_file):
    """Downloads the file described by the torrent."""
    if not os.path.exists(torrent_file):
        raise FileNotFoundError(f"Torrent file not found: {torrent_file}")

    session = lt.session()
    session.listen_on(6881, 6891)

    info = lt.torrent_info(torrent_file)
    params = {
        "save_path": "./",
        "storage_mode": lt.storage_mode_t.storage_mode_sparse,
        "ti": info,
    }

    handle = session.add_torrent(params)
    print(f"Starting download for: {info.name()}...")

    progress = tqdm(total=100, desc="Downloading", unit="%")
    while not handle.is_seed():
        status = handle.status()
        progress.n = int(status.progress * 100)
        progress.refresh()
        lt.sleep(1)

    progress.close()
    print(f"Download complete: {info.name()}")

def main():
    parser = argparse.ArgumentParser(description="LLM Torrent Orchestrator")
    parser.add_argument("--file", type=str, help="Path to the model weights file", required=True)
    parser.add_argument("--trackers", type=str, help="Path to a file containing tracker URLs", required=True)
    parser.add_argument("--download", action="store_true", help="Download the file described by the torrent")

    args = parser.parse_args()

    if args.download:
        download_torrent(args.file)
    else:
        if not os.path.exists(args.trackers):
            raise FileNotFoundError(f"Trackers file not found: {args.trackers}")

        with open(args.trackers, "r") as f:
            trackers = [line.strip() for line in f.readlines() if line.strip()]

        torrent_file = create_torrent(args.file, trackers)
        print(f"Torrent file created: {torrent_file}")

if __name__ == "__main__":
    main()