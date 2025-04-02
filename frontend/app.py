import tkinter as tk
import os
from tkinter import ttk, messagebox, filedialog
from typing import Optional
from backend.preset_manager import PresetManager
from backend.script_runner import ScriptRunner
from .components.preset_list import PresetList

class LineagePlusApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Lineage+")
        self.geometry("900x600")
        
        # Initialize backend
        self.preset_manager = PresetManager(presets_dir="presets", scripts_dir="scripts")
        self.script_runner = ScriptRunner()
        
        # Selected preset state
        self.current_preset: Optional[str] = None
        
        # UI Setup
        self._setup_ui()
        self._refresh_presets()

    def _setup_ui(self):
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left panel - Preset list (unchanged)
        left_panel = ttk.Frame(main_frame, width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        self.preset_list = PresetList(left_panel, on_preset_select=self._on_preset_select)
        self.preset_list.pack(fill=tk.BOTH, expand=True)

        # Right panel - Scripts for selected preset
        right_panel = ttk.LabelFrame(main_frame, text="Preset Scripts")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Script listbox with scrollbar
        self.script_listbox = tk.Listbox(
            right_panel,
            selectmode=tk.EXTENDED,
            height=10
        )
        scrollbar = ttk.Scrollbar(right_panel)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.script_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.script_listbox.yview)
        self.script_listbox.config(yscrollcommand=scrollbar.set)

        # Bottom control buttons
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(btn_frame, 
                text="New Preset", 
                command=self._new_preset).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, 
                text="Delete Preset", 
                command=self._delete_preset).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame, 
                text="Run Preset", 
                command=self._run_preset).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame,
                text="Add Script to Selected Preset",
                command=self._add_script_to_preset).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(btn_frame,
                text="Remove Selected Script",
                command=self._remove_selected_script).pack(side=tk.LEFT, padx=5)

    def _refresh_presets(self):
        """Reload presets from disk"""
        self.preset_list.update_items(self.preset_manager.list_presets())

    def _refresh_script_list(self):
        """Update the right panel with current preset's scripts (showing only filenames)"""
        self.script_listbox.delete(0, tk.END)
        
        if self.current_preset:
            preset = self.preset_manager.load_preset(self.current_preset)
            for full_path in preset.get('scripts', []):
                # Extract just the filename
                filename = os.path.basename(full_path)
                self.script_listbox.insert(tk.END, filename)
                
                # Store full path as hidden data
                self.script_listbox.itemconfig(
                    tk.END,
                    {'bg': 'white', 'fg': 'black', 'data': full_path}
                )

    def _add_script_to_preset(self):
        if not self.current_preset:
            messagebox.showwarning("No Preset Selected", "Please select a preset first")
            return
        
        filepaths = filedialog.askopenfilenames(
            initialdir=self.preset_manager.scripts_dir,
            title="Select Script",
            filetypes=[("AutoHotKey", "*.ahk"), ("All Files", "*.*")]
        )
        
        if filepaths:
            preset = self.preset_manager.load_preset(self.current_preset)
            scripts = preset.get('scripts', [])
            
            for full_path in filepaths:
                if full_path not in scripts:
                    scripts.append(full_path)
            
            self.preset_manager.save_preset(self.current_preset, scripts)
            self._refresh_script_list()


    def _remove_selected_script(self):
        if not self.current_preset:
            return
            
        selected = self.script_listbox.curselection()
        if not selected:
            return
            
        preset = self.preset_manager.load_preset(self.current_preset)
        scripts = preset.get('scripts', [])
        
        # Get full paths from listbox data
        to_remove = [self.script_listbox.get(i) for i in selected]
        
        # Filter out the selected scripts by comparing basenames
        scripts = [
            path for path in scripts 
            if os.path.basename(path) not in to_remove
        ]
    
        self.preset_manager.save_preset(self.current_preset, scripts)
        self._refresh_script_list()

    def _on_preset_select(self, preset_name: str):
        """Handle preset selection"""
        self.current_preset = preset_name
        self._refresh_script_list()
        print(f"Selected: {preset_name}")  # Replace with actual details display

    def _new_preset(self):
        """Create empty preset"""
        dialog = tk.Toplevel(self)
        dialog.title("New Preset")
        
        ttk.Label(dialog, text="Preset Name:").pack(pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.pack(pady=5)
        
        def save():
            name = name_entry.get()
            if not name:
                messagebox.showerror("Error", "Preset name cannot be empty!")
                return
                
            # Save empty preset
            self.preset_manager.save_preset(name, scripts=[])
            self._refresh_presets()
            dialog.destroy()
        
        ttk.Button(dialog, text="Save", command=save).pack(pady=10)

    def _run_preset(self):
        """Execute the selected preset"""
        if not self.current_preset:
            messagebox.showwarning("No Preset Selected", "Please select a preset first")
            return
            
        preset = self.preset_manager.load_preset(self.current_preset)
        if preset:
            self.script_runner.run_scripts(preset['scripts'])
            messagebox.showinfo("Success", f"Running {self.current_preset}!")

    def _delete_preset(self):
        """Remove selected preset"""
        if not self.current_preset:
            return
            
        if messagebox.askyesno(
            "Confirm Delete", 
            f"Delete preset '{self.current_preset}'?"
        ):
            self.preset_manager.delete_preset(self.current_preset)
            self.current_preset = None
            self._refresh_presets()