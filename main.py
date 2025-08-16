from pathlib import Path
from datetime import datetime
import csv
import json

def scan_directory(folder_path):
    """
    Recursively scan a folder and returns information about each file.

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
    
            
def classify_files(files):
    """
    Classify files as active, stale, or dark based on last modified date. 

    Parameters: 
        files (list of dict): Output from scan_directory()

    Returns: 
        list of dict: Same as input but with an added 'status' key
    """

    now = datetime.now()

    for file in files:
        age_days = (now - file["last_modified"]).days

        if age_days <= 30:
            status = "Active"
        elif 30 < age_days <= 180:
            status = "Stale"
        else: 
            status = "Dark"

        file["status"] = status
        
    return files

def export_to_csv(files, filename ="classified_files.csv"):
    """
    Export the list of classified files to a CSV file.

    Parameters:
        files (list of dict): Output from classify_files()
        filename (str): Name of the CSV file to create
    """

    # Define CSV column headers
    fieldnames = ["path", "size_mb", "last_modified", "status"]

    with open(filename, mode="w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
        writer.writeheader()
        for file in files: 
            # Convert datetime to string for CSV
            row = file.copy()
            row["last_modified"] = row["last_modified"].strftime("%Y-%m-%d %H:%M:%S")
            writer.writerow(row)

    print(f"Exported {len(files)} files to {filename}")


def export_to_json(files, filename="classified_files.json"):
    """
    Export the list of classified files to a JSON file.

    Parameters:
        files (list of dict): Output from classify_files()
        filename (str): Name of the JSON file to create
    """

    # Convert datetime to string
    files_serialisable = []
    for f in files:
        temp = f.copy()
        temp["last_modified"] = temp["last_modified"].strftime("%Y-%m-%d %H:%M:%S")
        files_serialisable.append(temp)

    with open(filename, "w", encoding="utf-8") as jsonfile:
        json.dump(files_serialisable, jsonfile, indent=4)

    print(f"Exported {len(files)} files to {filename}")

if __name__ == "__main__":
    files = scan_directory(".")
    classified_files = classify_files(files)

    for f in classified_files:
        print(f)

    export_to_csv(classified_files)
    export_to_json(classified_files)