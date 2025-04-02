import subprocess
from typing import List

class ScriptRunner:
    @staticmethod
    def run_scripts(paths: List[str]):
        """Execute multiple scripts with error handling"""
        processes = []
        for path in paths:
            try:
                if path.endswith('.ahk'):
                    proc = subprocess.Popen(['autohotkey.exe', path])
                else:
                    proc = subprocess.Popen(path)
                processes.append(proc)
            except Exception as e:
                print(f"Failed to launch {path}: {e}")
        return processes