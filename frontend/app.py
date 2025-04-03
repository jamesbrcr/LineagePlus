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
        
        # First set the color variables
        self._setup_colors()
        
        # Then configure styles (which uses the colors)
        self._configure_styles()
        
        # Then proceed with rest of initialization
        self.title("Lineage+")
        self.geometry("1200x800")
        self.configure(bg=self.bg_color)
        
        # Initialize backend services
        self.preset_manager = PresetManager(presets_dir="presets", scripts_dir="scripts")
        self.script_runner = ScriptRunner()
        
        # State management
        self.current_preset: Optional[str] = None
        
        # UI Setup
        self._setup_ui()
        self._refresh_presets()

    def _setup_colors(self):
        """Define all color variables"""
        self.bg_color = "#1a1a1a"
        self.frame_bg = "#2d2d2d"
        self.text_color = "#ffffff"
        self.accent_color = "#4a00e0"
        self.button_color = "#4a00e0"
        self.button_hover = "#6a1b9a"

    def _configure_styles(self):
        """Configure ttk styles for dark theme"""
        style = ttk.Style()
        
        # Frame styles
        style.configure('TFrame', background=self.bg_color)
        style.configure('Custom.TFrame', background=self.frame_bg)
        
        # Label styles
        style.configure(
            'TLabel',
            background=self.bg_color,
            foreground=self.text_color,
            font=('Arial', 10)
        )
        
        # Button styles
        style.configure(
            'TButton',
            background=self.button_color,
            foreground=self.text_color,
            borderwidth=0,
            font=('Arial', 10)
        )
        style.map(
            'TButton',
            background=[('active', self.button_hover)],
            foreground=[('active', self.text_color)]
        )
        
        # Treeview style
        style.configure('Preset.Treeview', 
                       background=self.frame_bg,
                       foreground=self.text_color,
                       fieldbackground=self.frame_bg)
        style.map('Preset.Treeview',
                 background=[('selected', self.accent_color)])

    def _setup_ui(self):
        """Initialize all UI components with new design"""
        # Header
        self._create_header()
        
        # Main container with 3 boxes
        self._create_main_panels()
        
        # Bottom control panel
        self._create_bottom_panel()

    def _create_header(self):
        """Create the Lineage+ header"""
        header_frame = tk.Frame(self, bg=self.bg_color)
        header_frame.pack(fill=tk.X, padx=20, pady=(20, 10))
        
        title_label = tk.Label(
            header_frame,
            text="LINEAGE+",
            font=("Arial", 24, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        title_label.pack(side=tk.LEFT)
        
        # Add any additional header elements here if needed

    def _create_main_panels(self):
        """Create the 3 main panels (Presets, Scripts, Overlays)"""
        main_frame = tk.Frame(self, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Configure grid weights
        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_columnconfigure(2, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        
        # Panel 1: Presets
        self._create_panel_with_header(
            main_frame, 
            "Presets", 
            0, 
            self._setup_preset_panel,
            add_cmd=self._new_preset,
            remove_cmd=self._delete_preset
        )
        
        # Panel 2: Scripts
        self._create_panel_with_header(
            main_frame, 
            "Scripts", 
            1, 
            self._setup_script_panel,
            add_cmd=self._add_script_to_preset,
            remove_cmd=self._remove_selected_script
        )
        
        # Panel 3: Overlays
        self._create_panel_with_header(
            main_frame, 
            "Overlays", 
            2, 
            self._setup_overlay_panel,
            add_cmd=lambda: self.overlay_manager.add_overlay(),
            remove_cmd=lambda: self.overlay_manager.remove_selected_overlay()
        )

    def _create_panel_with_header(self, parent, title, column, content_func, add_cmd, remove_cmd):
        """Helper to create a consistent panel with header and buttons"""
        panel_frame = tk.Frame(parent, bg=self.frame_bg, bd=0, highlightthickness=0)
        panel_frame.grid(row=0, column=column, sticky="nsew", padx=10, pady=5)
        
        # Header with title and buttons
        header = tk.Frame(panel_frame, bg=self.frame_bg)
        header.pack(fill=tk.X, padx=5, pady=5)
        
        title_label = tk.Label(
            header,
            text=title.upper(),
            font=("Arial", 10, "bold"),
            fg=self.text_color,
            bg=self.frame_bg
        )
        title_label.pack(side=tk.LEFT)
        
        # Add and remove buttons
        btn_frame = tk.Frame(header, bg=self.frame_bg)
        btn_frame.pack(side=tk.RIGHT)
        
        add_btn = tk.Button(
            btn_frame,
            text="+",
            font=("Arial", 8, "bold"),
            width=2,
            bg=self.button_color,
            fg=self.text_color,
            activebackground=self.button_hover,
            activeforeground=self.text_color,
            relief=tk.FLAT,
            command=add_cmd
        )
        add_btn.pack(side=tk.LEFT, padx=2)
        
        remove_btn = tk.Button(
            btn_frame,
            text="-",
            font=("Arial", 8, "bold"),
            width=2,
            bg="#d32f2f",
            fg=self.text_color,
            activebackground="#b71c1c",
            activeforeground=self.text_color,
            relief=tk.FLAT,
            command=remove_cmd
        )
        remove_btn.pack(side=tk.LEFT, padx=2)
        
        # Panel content
        content_func(panel_frame)

    def _setup_preset_panel(self, parent):
        """Presets panel content"""
        self.preset_list = PresetList(
            parent, 
            on_preset_select=self._on_preset_select
        )
        self.preset_list.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

    def _setup_script_panel(self, parent):
        """Scripts panel content"""
        # Script listbox with scrollbar
        list_frame = tk.Frame(parent, bg=self.frame_bg)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.script_listbox = tk.Listbox(
            list_frame,
            selectmode=tk.EXTENDED,
            bg=self.frame_bg,
            fg=self.text_color,
            selectbackground=self.accent_color,
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )
        self.script_listbox.pack(fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.script_listbox.yview)

    def _setup_overlay_panel(self, parent):
        """Overlays panel content"""
        self.overlay_manager = OverlayManager(self)
        self.overlay_manager.create_ui(parent)

    def _create_bottom_panel(self):
        """Create the bottom panel with preset info and control buttons"""
        bottom_frame = tk.Frame(self, bg=self.bg_color)
        bottom_frame.pack(fill=tk.X, padx=20, pady=(10, 20))
        
        # Current preset info
        self.current_preset_label = tk.Label(
            bottom_frame,
            text="No preset selected",
            font=("Arial", 10),
            fg=self.text_color,
            bg=self.bg_color
        )
        self.current_preset_label.pack(side=tk.LEFT, padx=10)
        
        # Control buttons
        btn_frame = tk.Frame(bottom_frame, bg=self.bg_color)
        btn_frame.pack(side=tk.RIGHT, padx=10)
        
        # Play button
        self.play_btn = tk.Button(
            btn_frame,
            text="▶",
            font=("Arial", 10, "bold"),
            width=3,
            bg="#2e7d32",
            fg=self.text_color,
            activebackground="#1b5e20",
            activeforeground=self.text_color,
            relief=tk.FLAT,
            command=self._run_preset
        )
        self.play_btn.pack(side=tk.LEFT, padx=5)
        
        # Pause button
        self.pause_btn = tk.Button(
            btn_frame,
            text="⏸",
            font=("Arial", 10, "bold"),
            width=3,
            bg="#ff8f00",
            fg=self.text_color,
            activebackground="#e65100",
            activeforeground=self.text_color,
            relief=tk.FLAT,
            command=self._pause_preset
        )
        self.pause_btn.pack(side=tk.LEFT, padx=5)
        
        # Stop button
        self.stop_btn = tk.Button(
            btn_frame,
            text="⏹",
            font=("Arial", 10, "bold"),
            width=3,
            bg="#c62828",
            fg=self.text_color,
            activebackground="#b71c1c",
            activeforeground=self.text_color,
            relief=tk.FLAT,
            command=self._stop_preset
        )
        self.stop_btn.pack(side=tk.LEFT, padx=5)

    # Preset Management Methods (unchanged from original)
    def _refresh_presets(self):
        """Reload presets from disk"""
        self.preset_list.update_items(self.preset_manager.list_presets())

    def _on_preset_select(self, preset_name: str):
        """Handle preset selection"""
        self.current_preset = preset_name
        self.current_preset_label.config(text=f"Selected: {preset_name}")
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
        dialog.configure(bg=self.bg_color)
        
        tk.Label(
            dialog, 
            text="Preset Name:", 
            bg=self.bg_color, 
            fg=self.text_color
        ).pack(pady=5)
        
        name_entry = tk.Entry(
            dialog, 
            bg=self.frame_bg, 
            fg=self.text_color,
            insertbackground=self.text_color
        )
        name_entry.pack(pady=5)
        
        def save():
            name = name_entry.get()
            if name:
                self.preset_manager.save_preset(name, scripts=[])
                self._refresh_presets()
                dialog.destroy()
        
        tk.Button(
            dialog, 
            text="Save", 
            command=save,
            bg=self.button_color,
            fg=self.text_color,
            activebackground=self.button_hover,
            activeforeground=self.text_color,
            relief=tk.FLAT
        ).pack(pady=10)

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
            self.current_preset_label.config(text="No preset selected")
            self._refresh_presets()

    # Script Management Methods (unchanged from original)
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

    def _pause_preset(self):
        """Pause the currently running preset"""
        # Implement your pause functionality here
        messagebox.showinfo("Info", "Preset paused")

    def _stop_preset(self):
        """Stop the currently running preset"""
        # Implement your stop functionality here
        messagebox.showinfo("Info", "Preset stopped")