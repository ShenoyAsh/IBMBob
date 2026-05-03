"""A module for managing JSON data files."""
import json
import os

class DataManager:
    """Handles loading and saving of structured data."""
    
    def __init__(self, base_path: str):
        """Initialize with a base directory."""
        self.base_path = base_path
        if not os.path.exists(base_path):
            os.makedirs(base_path)
            
    def save_data(self, filename: str, data: dict) -> bool:
        """Save a dictionary to a JSON file."""
        if not filename.endswith(".json"):
            filename += ".json"
            
        full_path = os.path.join(self.base_path, filename)
        try:
            with open(full_path, "w") as f:
                json.dump(data, f, indent=4)
            return True
        except Exception:
            return False

    def load_data(self, filename: str) -> dict:
        """Load data from a JSON file."""
        full_path = os.path.join(self.base_path, filename)
        if not os.path.exists(full_path):
            raise FileNotFoundError(f"No data found at {full_path}")
            
        with open(full_path, "r") as f:
            return json.load(f)

def process_records(records: list[dict], key: str) -> list:
    """Extract a specific key from a list of records."""
    if not records:
        return []
    return [r.get(key) for r in records if key in r]
