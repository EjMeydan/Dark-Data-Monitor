from pathlib import Path
from datetime import datetime

def scan_directory(folder_path):
    folder = Path(folder_path)

    if not folder.exists():
        print(f"Path {folder_path} does not exist.")
        return
    
    for file in folder.rglob("*"):
        if file.is_file():
            stats = file.stat()
            size_mb = stats.st_size / (1024 * 1024)
            last_modified = datetime.fromtimestamp(stats.st_mtime)

            print(f"{file} | {size_mb:.2f} MB | Last modified: {last_modified}")


if __name__ == "__main__":
    scan_directory(".")