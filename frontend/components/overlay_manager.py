import tkinter as tk
from tkinter import ttk, filedialog
import os
from typing import Dict, Tuple

class OverlayManager:
    def __init__(self, master):
        self.master = master
        self.active_overlays: Dict[str, Tuple[tk.Toplevel, tk.Label, bool]] = {}
    
    def create_ui(self, parent):
        frame = ttk.LabelFrame(parent, text="Overlay Manager")
        frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.listbox = tk.Listbox(frame, height=4)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        
        btn_frame = ttk.Frame(frame)
        btn_frame.pack(fill=tk.X)
        
        ttk.Button(btn_frame, text="Add", command=self._add_overlay).pack(side=tk.LEFT, expand=True)
        ttk.Button(btn_frame, text="Remove", command=self._remove_overlay).pack(side=tk.LEFT, expand=True)
        ttk.Button(btn_frame, text="Toggle", command=self._toggle_overlay).pack(side=tk.LEFT, expand=True)
    
    def _add_overlay(self):
        filepath = filedialog.askopenfilename(filetypes=[("PNG", "*.png")])
        if filepath:
            self._create_overlay(filepath)
            self.listbox.insert(tk.END, os.path.basename(filepath))
    
    def _create_overlay(self, image_path):
        overlay = tk.Toplevel(self.master)
        overlay.overrideredirect(True)
        overlay.attributes("-topmost", True)
        overlay.attributes("-transparentcolor", "white")
        
        try:
            img = tk.PhotoImage(file=image_path)
            label = tk.Label(overlay, image=img, bg="white")
            label.image = img
            label.pack()
            
            # Center initially
            overlay.geometry(f"+{self.master.winfo_screenwidth()//2}+{self.master.winfo_screenheight()//2}")
            
            # Make draggable
            label.bind("<Button-1>", lambda e: self._start_drag(e, overlay))
            label.bind("<B1-Motion>", lambda e: self._do_drag(e, overlay))
            
            self.active_overlays[image_path] = (overlay, label, False)
        except Exception as e:
            print(f"Error loading overlay: {e}")
    
    def _start_drag(self, event, window):
        window._drag_start_x = event.x
        window._drag_start_y = event.y
    
    def _do_drag(self, event, window):
        x = window.winfo_x() + (event.x - window._drag_start_x)
        y = window.winfo_y() + (event.y - window._drag_start_y)
        window.geometry(f"+{x}+{y}")
    
    def _remove_overlay(self):
        selected = self.listbox.curselection()
        if selected:
            filepath = self.listbox.get(selected[0])
            if filepath in self.active_overlays:
                self.active_overlays[filepath][0].destroy()
                del self.active_overlays[filepath]
            self.listbox.delete(selected[0])
    
    def _toggle_overlay(self):
        selected = self.listbox.curselection()
        if selected:
            filepath = self.listbox.get(selected[0])
            if filepath in self.active_overlays:
                overlay, label, hidden = self.active_overlays[filepath]
                if hidden:
                    overlay.deiconify()
                else:
                    overlay.withdraw()
                self.active_overlays[filepath] = (overlay, label, not hidden)