import tkinter as tk

class ToolTip:
    def __init__(self, widget, text, delay=500):
        self.widget = widget
        self.text = text
        self.delay = delay
        self.tooltip_window = None
        self._after_id = None
        self._visible = False

        self.widget.bind("<Enter>", self.on_enter)
        self.widget.bind("<Leave>", self.on_leave)
        self.widget.bind("<Motion>", self.on_motion)

    def on_enter(self, event=None):
        self.schedule()

    def on_leave(self, event=None):
        self.cancel()
        self.hide_tooltip()

    def on_motion(self, event=None):
        # Only reset if not currently showing tooltip
        if not self._visible:
            self.cancel()
            self.schedule()

    def schedule(self):
        self._after_id = self.widget.after(self.delay, self.show_tooltip)

    def cancel(self):
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None

    def show_tooltip(self):
        if self.tooltip_window or not self.widget.winfo_ismapped():
            return

        self._visible = True
        x = self.widget.winfo_rootx() + 0 - len(self.text) #center on button
        y = self.widget.winfo_rooty() - 30

        self.tooltip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")

        label = tk.Label(
            tw,
            text=self.text,
            justify="left",
            background="#2a2a2a",
            foreground="white",
            relief="solid",
            borderwidth=0,
            font=("Arial", 10)
        )
        label.pack(ipadx=6, ipady=2)

    def hide_tooltip(self, event=None):
        self._visible = False
        if self._after_id:
            self.widget.after_cancel(self._after_id)
            self._after_id = None
        if self.tooltip_window:
            self.tooltip_window.destroy()
            self.tooltip_window = None

