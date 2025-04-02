import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
import pyautogui

class AutoClicker:
    def __init__(self, master):
        self.master = master
        self.clicking = False
        self.click_thread = None
        self.cps = 10  # Default clicks per second
        self.hotkey = "F6"  # Default toggle key (must be valid Tkinter keysym)
        self.hotkey_var = tk.StringVar(value=self.hotkey)

    def create_ui(self, parent):
        """Build autoclicker UI"""
        frame = ttk.LabelFrame(parent, text="AutoClicker")
        frame.pack(fill=tk.X, padx=5, pady=5)

        # CPS Control
        ttk.Label(frame, text="CPS (1-20):").grid(row=0, column=0, sticky="w")
        self.cps_spin = ttk.Spinbox(
            frame,
            from_=1,
            to=20,
            width=5
        )
        self.cps_spin.set(self.cps)
        self.cps_spin.grid(row=0, column=1, sticky="w", padx=5)

        # Hotkey Binding
        ttk.Label(frame, text="Toggle Key:").grid(row=1, column=0, sticky="w")
        self.hotkey_entry = ttk.Combobox(
            frame,
            textvariable=self.hotkey_var,
            values=[
                'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 
                'F7', 'F8', 'F9', 'F10', 'F11', 'F12'
            ],
            width=5,
            state="readonly"
        )
        self.hotkey_entry.grid(row=1, column=1, sticky="w", padx=5)

        # Status Indicator
        self.status_var = tk.StringVar(value="❌ OFF")
        ttk.Label(frame, textvariable=self.status_var).grid(row=2, columnspan=2)

        # Control Buttons
        btn_frame = ttk.Frame(frame)
        btn_frame.grid(row=3, columnspan=2, pady=5)

        ttk.Button(
            btn_frame,
            text="Start",
            command=self.start_clicking
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            btn_frame,
            text="Stop",
            command=self.stop_clicking
        ).pack(side=tk.LEFT, padx=5)

        # Initialize binding
        self.update_hotkey_binding()

    def update_hotkey_binding(self):
        """Update the hotkey binding"""
        try:
            # Remove old binding
            if hasattr(self, '_current_hotkey'):
                self.master.unbind(f"<KeyPress-{self._current_hotkey}>")
            
            # Set new binding
            self._current_hotkey = self.hotkey_var.get().upper()
            self.master.bind(f"<KeyPress-{self._current_hotkey}>", lambda e: self.toggle_clicking())
        except tk.TclError as e:
            messagebox.showerror("Binding Error", f"Invalid key: {str(e)}")

    def toggle_clicking(self):
        """Toggle autoclicker with hotkey"""
        if self.clicking:
            self.stop_clicking()
        else:
            self.start_clicking()

    def start_clicking(self):
        """Start autoclicker thread"""
        if not self.clicking:
            try:
                self.cps = min(20, max(1, int(self.cps_spin.get())))
                self.hotkey = self.hotkey_var.get().upper()
                self.update_hotkey_binding()
                
                self.clicking = True
                self.status_var.set("✅ ON")
                self.click_thread = threading.Thread(
                    target=self._click_loop, 
                    daemon=True
                )
                self.click_thread.start()
            except ValueError:
                messagebox.showerror("Error", "Please enter a valid CPS (1-20)")

    def stop_clicking(self):
        """Stop autoclicker"""
        self.clicking = False
        self.status_var.set("❌ OFF")

    def _click_loop(self):
        """Main clicking loop"""
        delay = 1 / self.cps
        while self.clicking:
            pyautogui.click()
            time.sleep(delay)