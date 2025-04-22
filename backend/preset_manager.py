import os # for file operations
import sys
import json # for data serialization and file reading
import shutil # for file movement and removal
from datetime import datetime # for timestamping
from typing import Dict, List, Optional


def get_base_path():
    import sys
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)  # Running from .exe
    return os.path.dirname(os.path.abspath(__file__))  # Running from source

# Class to manage presets. Allows the user to add various files to the preset to automatically run them
class PresetManager:
    def __init__(self, presets_dir: str = "presets", scripts_dir: str = "scripts"):
        base_dir = get_base_path()
        self.presets_dir = os.path.join(base_dir, presets_dir)
        self.scripts_dir = os.path.join(base_dir, scripts_dir)
        self._ensure_directories_exist()
    
    def _ensure_directories_exist(self):
        os.makedirs(self.presets_dir, exist_ok=True)
        os.makedirs(self.scripts_dir, exist_ok=True)  

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
        data = {
            "scripts": scripts,
            "created": datetime.now().isoformat(),
            **metadata
        }
        try:
            path = os.path.join(self.presets_dir, f"{name}.json")
            #print(f"Saving preset to: {path}")
            with open(path, 'w') as f:
                json.dump(data, f, indent=2)
            #print("Preset saved successfully.")
        except Exception as e:
            #print(f"Error saving preset: {e}")
            raise

    def delete_preset(self, name: str):
        """Remove a preset file"""
        os.remove(os.path.join(self.presets_dir, f"{name}.json"))

    def list_scripts(self, preset_name):
        # Return list of .ahk scripts for a preset
        preset_path = os.path.join(self.presets_dir, f"{preset_name}.json")
        if os.path.exists(preset_path):
            with open(preset_path, 'r') as f:
                data = json.load(f)
                return data.get("scripts", [])
        return []

    def add_script_to_preset(self, preset_name, script_path):
        script_filename = os.path.basename(script_path)
        destination_path = os.path.join(self.scripts_dir, script_filename)

        #print(f"Selected script: {script_path}")
        #print(f"Copying to: {destination_path}")

        if not os.path.exists(destination_path):
            shutil.copy2(script_path, destination_path)

        scripts = self.list_scripts(preset_name)
        if script_filename not in scripts:
            scripts.append(script_filename)
            self.save_preset(preset_name, scripts)

    def delete_script(self, name: str):
        """Remove a script file"""
        path = os.path.join(self.scripts_dir, name)
        #print(f"Trying to delete: {path}")
        if not os.path.exists(path):
            raise FileNotFoundError(f"Script file does not exist: {path}")
        os.remove(path)

    def remove_script_from_preset(self, preset_name: str, script_name: str):
        """Remove a script reference from the specified preset without deleting the actual script file."""
        preset_path = os.path.join(self.presets_dir, f"{preset_name}.json")
        if os.path.exists(preset_path):
            with open(preset_path, "r") as f:
                data = json.load(f)

            scripts = data.get("scripts", [])
            if script_name in scripts:
                scripts.remove(script_name)
                data["scripts"] = scripts

                with open(preset_path, "w") as f:
                    json.dump(data, f, indent=2)
