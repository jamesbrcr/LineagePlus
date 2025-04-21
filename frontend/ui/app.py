import customtkinter as ctk

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Window configuration
        self.title("LINEAGE+")
        self.geometry("800x600")  # Adjust window size as needed
        self.resizable(False, False)

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Presets column
        self.grid_columnconfigure(1, weight=2)  # Main content area

        # Left frame for Presets
        self.presets_frame = ctk.CTkFrame(self, fg_color="black")
        self.presets_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.presets_frame.grid_rowconfigure(0, weight=1)

        presets_label = ctk.CTkLabel(self.presets_frame, text="Presets", font=("Helvetica", 16))
        presets_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="nw")

        # Main content area (right side)
        self.main_frame = ctk.CTkFrame(self, fg_color="black")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)
        
        # Configure grid for main content area
        self.main_frame.grid_rowconfigure(0, weight=1)  # Scripts section
        self.main_frame.grid_rowconfigure(1, weight=1)  # Overlays section
        self.main_frame.grid_rowconfigure(2, weight=1)  # Cooldowns section
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Scripts frame
        scripts_label = ctk.CTkLabel(self.main_frame, text="Scripts", font=("Helvetica", 16))
        scripts_label.grid(row=0, column=0, padx=(10, 10), pady=(10, 5), sticky="nw")

        scripts_frame = ctk.CTkFrame(self.main_frame)
        scripts_frame.grid(row=0, column=0, sticky="nsew", padx=(10, 10), pady=(30, 5))

        # Overlays frame
        overlays_label = ctk.CTkLabel(self.main_frame, text="Overlays", font=("Helvetica", 16))
        overlays_label.grid(row=1, column=0, padx=(10, 10), pady=(20, 5), sticky="nw")

        overlays_frame = ctk.CTkFrame(self.main_frame)
        overlays_frame.grid(row=1, column=0, sticky="nsew", padx=(10, 10), pady=(30, 5))

        # Cooldowns frame
        cooldowns_label = ctk.CTkLabel(self.main_frame, text="Cooldowns", font=("Helvetica", 16))
        cooldowns_label.grid(row=2, column=0, padx=(10, 10), pady=(20, 5), sticky="nw")

        cooldowns_frame = ctk.CTkFrame(self.main_frame)
        cooldowns_frame.grid(row=2, column=0, sticky="nsew", padx=(10, 10), pady=(30, 5))

if __name__ == "__main__":
    app = App()
    app.mainloop()
