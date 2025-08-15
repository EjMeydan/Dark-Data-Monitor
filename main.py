from pathlib import Path
from datetime import datetime

def scan_directory(folder_path):
    """
    Recursively scan a folder and prints information about each file.

    Parameters: 
    folder_path (str): The path to the folder to scan

    Returns:
        list of dict: Each dictionary constains:
            - 'path': str, full file path
            - 'size_mb': float, file size in megabytes
            - 'last_modified': datetime, last modified timestamp
    """

    folder = Path(folder_path)

    if not folder.exists():
        print(f"Path {folder_path} does not exist.")
        return []
    
    files_data = []
    
    for file in folder.rglob("*"): # Recursively list all files
        if file.is_file():
            
            stats = file.stat()
            size_mb = stats.st_size / (1024 * 1024) # Convert bytes to MB
            last_modified = datetime.fromtimestamp(stats.st_mtime) 

            # Store file info in a dictionary
            files_data.append({
                "path": str(file),
                "size_mb": size_mb,
                "last_modified": last_modified
            })
        
    return files_data 


if __name__ == "__main__":
    files = scan_directory(".")
    for f in files:
        print(f)