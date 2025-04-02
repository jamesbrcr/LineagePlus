import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
from typing import Optional
from backend.preset_manager import PresetManager
from backend.script_runner import ScriptRunner
from .components.preset_list import PresetList
from .components.overlay_manager import OverlayManager
from .components.cooldown_tracker import CooldownTracker

class LineagePlusApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Lineage+")
        self.geometry("1200x600")
        
        # Initialize backend services
        self.preset_manager = PresetManager(presets_dir="presets", scripts_dir="scripts")
        self.script_runner = ScriptRunner()
        
        # State management
        self.current_preset: Optional[str] = None
        
        # UI Setup
        self._setup_ui()
        self._refresh_presets()

    def _setup_ui(self):
        """Initialize all UI components"""
        # Main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Left Panel - Presets
        self._setup_preset_panel(main_frame)
        
        # Middle Panel - Scripts
        self._setup_script_panel(main_frame)
        
        # Right Panel - Tools
        self._setup_tools_panel(main_frame)
        
        # Bottom Control Buttons
        self._setup_control_buttons()

    def _setup_preset_panel(self, parent):
        """Left panel with preset list"""
        left_panel = ttk.Frame(parent, width=200)
        left_panel.pack(side=tk.LEFT, fill=tk.Y)
        
        self.preset_list = PresetList(
            left_panel, 
            on_preset_select=self._on_preset_select
        )
        self.preset_list.pack(fill=tk.BOTH, expand=True)

    def _setup_script_panel(self, parent):
        """Middle panel with script list"""
        middle_panel = ttk.LabelFrame(parent, text="Preset Scripts")
        middle_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Script listbox with scrollbar
        self.script_listbox = tk.Listbox(
            middle_panel,
            selectmode=tk.EXTENDED,
            height=10
        )
        scrollbar = ttk.Scrollbar(middle_panel)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.script_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.script_listbox.yview)
        self.script_listbox.config(yscrollcommand=scrollbar.set)

    def _setup_tools_panel(self, parent):
        """Right panel with tools"""
        right_panel = ttk.Frame(parent, width=300)
        right_panel.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Initialize and pack tools
        self.overlay_manager = OverlayManager(self)
        self.cooldown_tracker = CooldownTracker(self)
        
        self.overlay_manager.create_ui(right_panel)
        self.cooldown_tracker.create_ui(right_panel)

    def _setup_control_buttons(self):
        """Bottom control buttons"""
        btn_frame = ttk.Frame(self)
        btn_frame.pack(fill=tk.X, padx=10, pady=5)
        
        buttons = [
            ("New Preset", self._new_preset),
            ("Delete Preset", self._delete_preset),
            ("Run Preset", self._run_preset),
            ("Add Script", self._add_script_to_preset),
            ("Remove Script", self._remove_selected_script)
        ]
        
        for text, cmd in buttons:
            ttk.Button(btn_frame, text=text, command=cmd).pack(side=tk.LEFT, padx=5)

    # Preset Management Methods
    def _refresh_presets(self):
        """Reload presets from disk"""
        self.preset_list.update_items(self.preset_manager.list_presets())

    def _on_preset_select(self, preset_name: str):
        """Handle preset selection"""
        self.current_preset = preset_name
        self._refresh_script_list()

    def _refresh_script_list(self):
        """Update script list for selected preset"""
        self.script_listbox.delete(0, tk.END)
        if self.current_preset:
            preset = self.preset_manager.load_preset(self.current_preset)
            for path in preset.get('scripts', []):
                self.script_listbox.insert(tk.END, os.path.basename(path))
                self.script_listbox.itemconfig(tk.END, {'data': path})

    def _new_preset(self):
        """Create new preset dialog"""
        dialog = tk.Toplevel(self)
        dialog.title("New Preset")
        
        ttk.Label(dialog, text="Preset Name:").pack(pady=5)
        name_entry = ttk.Entry(dialog)
        name_entry.pack(pady=5)
        
        def save():
            name = name_entry.get()
            if name:
                self.preset_manager.save_preset(name, scripts=[])
                self._refresh_presets()
                dialog.destroy()
        
        ttk.Button(dialog, text="Save", command=save).pack(pady=10)

    def _delete_preset(self):
        """Delete selected preset"""
        if not self.current_preset:
            return
            
        if messagebox.askyesno(
            "Confirm Delete", 
            f"Delete preset '{self.current_preset}'?"
        ):
            self.preset_manager.delete_preset(self.current_preset)
            self.current_preset = None
            self._refresh_presets()

    # Script Management Methods
    def _add_script_to_preset(self):
        """Add script to current preset"""
        if not self.current_preset:
            messagebox.showwarning("No Preset Selected", "Please select a preset first")
            return
            
        filepaths = filedialog.askopenfilenames(
            initialdir=self.preset_manager.scripts_dir,
            filetypes=[("AutoHotKey", "*.ahk"), ("All Files", "*.*")]
        )
        
        if filepaths:
            preset = self.preset_manager.load_preset(self.current_preset)
            scripts = preset.get('scripts', [])
            scripts.extend(path for path in filepaths if path not in scripts)
            self.preset_manager.save_preset(self.current_preset, scripts)
            self._refresh_script_list()

    def _remove_selected_script(self):
        """Remove selected scripts from current preset"""
        if not self.current_preset:
            return
            
        selected = self.script_listbox.curselection()
        if not selected:
            return
            
        preset = self.preset_manager.load_preset(self.current_preset)
        scripts = preset.get('scripts', [])
        
        # Remove selected scripts by full path
        to_remove = [self.script_listbox.itemcget(i, 'data') for i in selected]
        scripts = [path for path in scripts if path not in to_remove]
        
        self.preset_manager.save_preset(self.current_preset, scripts)
        self._refresh_script_list()

    def _run_preset(self):
        """Execute scripts in selected preset"""
        if not self.current_preset:
            messagebox.showwarning("No Preset Selected", "Please select a preset first")
            return
            
        preset = self.preset_manager.load_preset(self.current_preset)
        if preset:
            self.script_runner.run_scripts(preset['scripts'])
            messagebox.showinfo("Success", f"Running {self.current_preset}!")