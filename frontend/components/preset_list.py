import tkinter as tk
from tkinter import ttk
from typing import Callable, List

class PresetList(ttk.Frame):
    def __init__(self, master, on_preset_select: Callable = None, **kwargs):
        super().__init__(master, **kwargs)
        self.on_select = on_preset_select
        
        self.tree = ttk.Treeview(self, columns=('type'), show='tree', selectmode='browse')
        self.tree.heading('#0', text='Presets', anchor=tk.W)
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        self.tree.bind('<<TreeviewSelect>>', self._handle_selection)

    def update_items(self, presets: List[str]):
        """Refresh the list with new presets"""
        self.tree.delete(*self.tree.get_children())
        for preset in presets:
            self.tree.insert('', 'end', text=preset, values=('preset'))

    def _handle_selection(self, event):
        """Trigger callback when selection changes"""
        if self.on_select:
            selected = self.tree.selection()
            if selected:
                self.on_select(self.tree.item(selected[0])['text'])