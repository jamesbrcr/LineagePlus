import customtkinter as ctk

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

class LineagePlusApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("dark")

        self.configure(fg_color="#050505")  # Even darker gray

        # Window configuration
        self.title("LINEAGE+")
        self.geometry("600x500") 
        self.resizable(False, False)
        #self.configure(fg_color="#2b2b2b")

        # Main title label (added at top left)
        title_label = ctk.CTkLabel(
            master=self,
            text="Lineage+",
            font=("Arial", 36, "bold"),  # Larger and bold font
            text_color="#613DC1",  # Golden color to match your border
            anchor="w"  # Left-aligned
        )
        title_label.place(x=30, y=30)  # Positioned at top left with some padding


#"""PRESET SECTION"""

    #"""PRESET FRAME"""

        presetFrame = ctk.CTkFrame(
            master=self,
            fg_color="#090d0d",
            border_color="#613DC1",
            border_width=4,
            corner_radius=0, # UNDECIDED VISUAL CHANGE (rounded area or no)
            width=285,    # width
            height=380    # height
        )
        presetFrame.place(x=10, y=110)

    #"""PRESET HEADER"""

        # Header Label
        header_frame = ctk.CTkFrame(  # Changed from CTkLabel to CTkFrame
            master=presetFrame,
            fg_color="#858AE3",
            corner_radius=0,
            height=30,
            width = -8
        )
        header_frame.place(x=4, y=4, relwidth=0.97)

        # Header Text Label (added first so buttons appear on top)
        header_text = ctk.CTkLabel(
            master=header_frame,
            text="Presets",
            font=("Arial", 16, "bold"),
            text_color="#2C0735",  # Dark text for contrast
            anchor="w",  # Left-aligned
            fg_color="transparent",  # Transparent background
            height=30
        )
        header_text.place(x=10, y=0)  # 10px left padding

    #"""PRESET BUTTONS"""

        # Plus button (placed absolutely)
        preset_plus_btn = ctk.CTkButton(
            master=header_frame,
            text="+",
            text_color="#2C0735",
            font=("Arial", 18, "bold"),
            width=20,
            height=20,
            fg_color="transparent",
            hover_color="#613DC1",
            # command=self.add_preset
        )
        # Place it at vertical center, near the right edge
        preset_plus_btn.place(relx=1.0, rely=0.5, x=-32, anchor="e")

        # Minus button (placed absolutely)
        preset_minus_btn = ctk.CTkButton(
            master=header_frame,
            text="-",
            text_color="#2C0735",
            font=("Arial", 18, "bold"),
            width=25,
            height=20,
            fg_color="transparent",
            hover_color="#613DC1",
            # command=self.remove_preset
        )
        # Place it to the left of plus button, also centered vertically
        preset_minus_btn.place(relx=1.0, rely=0.5, x=-2, anchor="e")


#"""SCRIPTS SECTION"""

    #"""SCRIPTS FRAME"""
        # Right Frame (Scripts) - positioned to the right of presetFrame
        scriptsFrame = ctk.CTkFrame(
            master=self,
            fg_color="#090d0d",
            border_color="#613DC1",
            border_width=4,
            corner_radius=0, # UNDECIDED VISUAL CHANGE
            width=285,
            height=120
        )
        scriptsFrame.place(x=10 + 285 + 10, y=110)  # 10px gap from presetFrame

    #"""SCRIPTS HEADER"""

        # Header Label
        scripts_header_frame = ctk.CTkFrame(  # Changed from CTkLabel to CTkFrame
            master=scriptsFrame,
            fg_color="#858AE3",
            corner_radius=0,
            height=30,
            width = -8
        )
        scripts_header_frame.place(x=4, y=4, relwidth=0.97)

        # Header Text Label (added first so buttons appear on top)
        scripts_header_text = ctk.CTkLabel(
            master=scripts_header_frame,
            text="Scripts",
            font=("Arial", 16, "bold"),
            text_color="#2C0735",  # Dark text for contrast
            anchor="w",  # Left-aligned
            fg_color="transparent",  # Transparent background
            height=30
        )
        scripts_header_text.place(x=10, y=0)  # 10px left padding


#"""OVERLAYS SECTION"""


        # Right Frame (Scripts) - positioned to the right of presetFrame
        overlaysFrame = ctk.CTkFrame(
            master=self,
            fg_color="#8D6F3A",
            border_color="#FFCC70",
            border_width=2,
            width=285,
            height=120
        )
        overlaysFrame.place(x=10+285+10, y=110 + 110 + 10 + 10)  # 10px gap from presetFrame and below scriptsFram

        overlays_header_label = ctk.CTkLabel(
            master=overlaysFrame,
            text="Overlays",
            font=("Arial", 16),
            fg_color="#5D4A2A",
            height=30,
            corner_radius=0,
            anchor="w"
        )
        overlays_header_label.place(x=0, y=0, relwidth=1.0)


#"""COOLDOWNS SECTION"""


        # Right Frame (Scripts) - positioned to the right of presetFrame
        cooldownsFrame = ctk.CTkFrame(
            master=self,
            fg_color="#8D6F3A",
            border_color="#FFCC70",
            border_width=2,
            width=285,
            height=120
        )
        cooldownsFrame.place(x=10+285+10, y=110 + 110 + 110 + 10 + 10 + 10 + 10)  # 10px gap from presetFrame and below scriptsFram

        cooldowns_header_label = ctk.CTkLabel(
            master=cooldownsFrame,
            text="Cooldowns",
            font=("Arial", 16),
            fg_color="#5D4A2A",
            height=30,
            corner_radius=0,
            anchor="w"
        )
        cooldowns_header_label.place(x=0, y=0, relwidth=1.0)


if __name__ == "__main__":
    app = LineagePlusApp()
    app.mainloop()
