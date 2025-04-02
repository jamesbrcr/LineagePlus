import os # for file operations
import json # for data serialization and file reading
from datetime import datetime # for timestamping
from typing import Dict, List, Optional

# Class to manage presets. Allows the user to add various files to the preset to automatically run them
class PresetManager:
    def __init__(self, presets_dir: str = "presets", scripts_dir: str = "scripts"):
        self.presets_dir = presets_dir
        self.scripts_dir = scripts_dir  # Add this line
        self._ensure_directories_exist()
    
    def _ensure_directories_exist(self):
        os.makedirs(self.presets_dir, exist_ok=True)
        os.makedirs(self.scripts_dir, exist_ok=True)  # Add this line

    def list_presets(self) -> List[str]:
        """Return sorted list of preset names"""
        return sorted([
            f[:-5] for f in os.listdir(self.presets_dir) 
            if f.endswith('.json')
        ])

    def load_preset(self, name: str) -> Optional[Dict]:
        """Load preset data or return None if not found"""
        path = os.path.join(self.presets_dir, f"{name}.json")
        if not os.path.exists(path):
            return None
            
        with open(path, 'r') as f:
            return json.load(f)

    def save_preset(self, name: str, scripts: List[str], **metadata):
        """Save preset with additional metadata"""
        data = {
            "scripts": scripts,
            "created": datetime.now().isoformat(),
            **metadata
        }
        with open(os.path.join(self.presets_dir, f"{name}.json"), 'w') as f:
            json.dump(data, f, indent=2)

    def delete_preset(self, name: str):
        """Remove a preset file"""
        os.remove(os.path.join(self.presets_dir, f"{name}.json"))