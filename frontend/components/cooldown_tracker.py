import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Tuple

class CooldownTracker:
    def __init__(self, master):
        self.master = master
        self.active_trackers: Dict[str, Tuple[str, float]] = {}
    
    def create_ui(self, parent):
        frame = ttk.LabelFrame(parent, text="Cooldown Tracker")
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(frame, text="Ability:").grid(row=0, column=0, sticky="w")
        self.ability_entry = ttk.Entry(frame)
        self.ability_entry.grid(row=0, column=1, sticky="ew")
        
        ttk.Label(frame, text="Duration (s):").grid(row=1, column=0, sticky="w")
        self.duration_entry = ttk.Entry(frame)
        self.duration_entry.grid(row=1, column=1, sticky="ew")
        
        ttk.Label(frame, text="Key:").grid(row=2, column=0, sticky="w")
        self.key_entry = ttk.Entry(frame)
        self.key_entry.grid(row=2, column=1, sticky="ew")
        
        ttk.Button(frame, text="Start", command=self._start_tracker).grid(row=3, columnspan=2)
        
        self.tree = ttk.Treeview(frame, columns=("ability", "key", "duration"), show="headings", height=4)
        self.tree.heading("ability", text="Ability")
        self.tree.heading("key", text="Key")
        self.tree.heading("duration", text="Duration")
        self.tree.grid(row=4, columnspan=2, sticky="nsew")
        
        ttk.Button(frame, text="Remove", command=self._remove_tracker).grid(row=5, columnspan=2)
    
    def _start_tracker(self):
        ability = self.ability_entry.get()
        duration = self.duration_entry.get()
        key = self.key_entry.get().lower()
        
        if not all([ability, duration, key]):
            messagebox.showwarning("Missing Fields", "Please fill all fields")
            return
        
        try:
            duration_float = float(duration)
            self.active_trackers[key] = (ability, duration_float)
            self.tree.insert("", "end", values=(ability, key, duration))
            
            self.master.bind(
                f"<KeyPress-{key}>",
                lambda e, a=ability, d=duration_float: self._trigger_cooldown(a, d)
            )
            
            self.ability_entry.delete(0, tk.END)
            self.duration_entry.delete(0, tk.END)
            self.key_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Invalid Duration", "Please enter a valid number")
    
    def _trigger_cooldown(self, ability: str, duration: float):
        overlay = tk.Toplevel(self.master)
        overlay.overrideredirect(True)
        overlay.attributes("-topmost", True)
        overlay.attributes("-alpha", 0.8)
        
        ttk.Label(overlay, text=ability, font=("Arial", 14)).pack()
        time_label = ttk.Label(overlay, text=f"{duration:.1f}", font=("Arial", 24))
        time_label.pack()
        
        x, y = self.master.winfo_pointerxy()
        overlay.geometry(f"+{x+20}+{y+20}")
        
        self._countdown(overlay, time_label, duration)
    
    def _countdown(self, window, label, remaining):
        if remaining > 0:
            label.config(text=f"{remaining:.1f}")
            window.after(100, lambda: self._countdown(window, label, remaining-0.1))
        else:
            window.destroy()
    
    def _remove_tracker(self):
        selected = self.tree.selection()
        if selected:
            key = self.tree.item(selected[0])['values'][1]
            self.tree.delete(selected[0])
            self.master.unbind(f"<KeyPress-{key}>")
            del self.active_trackers[key]