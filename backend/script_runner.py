import subprocess
from typing import List
import psutil  # pip install psutil
import os

class ScriptRunner:

    def get_running_scripts(self):
        """
        Returns a set of currently running AHK script file paths.
        """
        running = set()

        for proc in psutil.process_iter(['name', 'cmdline']):
            if proc.info['name'] == 'AutoHotkey.exe':
                cmdline = proc.info.get('cmdline', [])
                for arg in cmdline:
                    if arg.lower().endswith('.ahk'):
                        running.add(os.path.abspath(arg))

        return running

    def run_scripts(self, scripts, scripts_dir):
        """
        Runs a list of AutoHotkey scripts from the specified directory.
        Returns a list of errors (if any).
        """
        errors = []
        running = self.get_running_scripts()

        for script_name in scripts:
            script_path = os.path.abspath(os.path.join(scripts_dir, script_name))
            if not os.path.exists(script_path):
                errors.append((script_name, "File not found"))
                continue

            if script_path in running:
                # Script is already running; skip it
                continue

            try:
                subprocess.Popen(["C:\\Program Files\\AutoHotkey\\AutoHotkey.exe", script_path])
            except Exception as e:
                errors.append((script_name, str(e)))

        return errors

    def stop_scripts(self):
        """
        Kills AutoHotkey scripts and returns a list of script filenames that were stopped.
        """
        stopped_scripts = []

        for proc in psutil.process_iter(['name', 'cmdline']):
            try:
                if proc.info['name'] == "AutoHotkey.exe":
                    cmdline = proc.info.get('cmdline', [])
                    for arg in cmdline:
                        if arg.lower().endswith('.ahk'):
                            script_name = os.path.basename(arg)
                            stopped_scripts.append(script_name)
                    proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return stopped_scripts