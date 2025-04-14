import customtkinter as ctk
from customtkinter import CTkImage
from CTkMessagebox import CTkMessagebox # pip install CTkMessagebox
import tkinter.filedialog as filedialog
from PIL import Image # pip install pillow
from backend.preset_manager import PresetManager
from backend.script_runner import ScriptRunner
import os

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
#ctk.set_default_color_theme("blue")

class LineagePlusApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.preset_manager = PresetManager(presets_dir="presets", scripts_dir="scripts")
        self.script_runner = ScriptRunner()

        self.current_preset = None
        self.preset_buttons = {}
        self.current_script = None
        self.script_buttons = {}


        ctk.set_appearance_mode("dark")
        self.configure(fg_color="#303030")  # Even darker gray

        # Window configuration
        self.title("LINEAGE+")
        self.geometry("600x500")
        self.resizable(False, False)
        

#"""IMAGE IMPORTS"""

        try:
            # Get absolute path to your image
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, "images", "healer_icon.png")
            
            healer_icon = Image.open(image_path)
            
            # Convert to CTkImage
            healer_image = CTkImage(
                light_image=healer_icon,
                dark_image=healer_icon,
                size=(60, 60)  # Adjust size as needed
            )

            #print("IMAGE LOADED!")

        except Exception as e:
            print(f"Error loading image: {e}")
            icon = None  # Fallback if image fails to load

        try:
            # Get absolute path to your image
            script_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(script_dir, "images", "LINEAGE_TITLE_NOBG.png")
            
            title_icon = Image.open(image_path)
            
            # Convert to CTkImage
            title_image = CTkImage(
                light_image=title_icon,
                dark_image=title_icon,
                size=(208, 34)  # Adjust size as needed
            )

            #print("IMAGE LOADED!")

        except Exception as e:
            print(f"Error loading image: {e}")
            icon = None  # Fallback if image fails to load


# MAIN HEADER
        header_container = ctk.CTkFrame(
            master=self,
            fg_color="transparent",
            height=100  # Match your title image height
        )
        header_container.pack(side="top", fill="x", padx=30, pady=30)  # Automatic width

        # TITLE IMAGE
        title_image_label = ctk.CTkLabel(
            master=header_container,
            image=title_image,
            text=""
        )
        title_image_label.pack(side="left")

        # PLUS SIGN
        plus_label = ctk.CTkLabel(
            master=header_container,
            text="+",
            font=("Arial", 60, "bold"),
            text_color="#FFFFFF"
        )
        plus_label.pack(side="left", padx=10)

    #"""MAIN BUTTONS"""

        # Plus button (placed absolutely)
        run_btn = ctk.CTkButton(
            master=header_container,
            text="run",
            text_color="#858AE3",
            font=("Arial", 18, "bold"),
            width=20,
            height=20,
            fg_color="transparent",
            hover_color="#613DC1",
            # corner_radius = 32, # CIRCULAR BUTTONS? WITH BORDERS?
            # command=self.add_preset
        )
        # Place it at vertical center, near the right edge
        run_btn.place(relx=1.0, rely=0.5, x=-62, anchor="e")

        # Minus button (placed absolutely)
        stop_btn = ctk.CTkButton(
            master=header_container,
            text="stop",
            text_color="#858AE3",
            font=("Arial", 18, "bold"),
            width=25,
            height=20,
            fg_color="transparent",
            hover_color="#613DC1",
            # command=self.remove_preset
        )
        # Place it to the left of plus button, also centered vertically
        stop_btn.place(relx=1.0, rely=0.5, x=-2, anchor="e")

    #"""HEALER ICON"""
        """
        healer_image_label = ctk.CTkLabel(
            master=header_container,
            image=healer_image,  # Your healer icon
            text=""  # No text
        )
        healer_image_label.pack(side="left", padx=(0, 10))  # 10px spacing between icon and text
        """
        """
        image_label = ctk.CTkLabel(
            master=title_label,
            image=healer_image,
            fg_color="transparent",
            text=""
        )
        image_label.place(x=140, y=10)
        """


#"""PRESETS SECTION"""

    #"""PRESET FRAME"""


        presetFrame = ctk.CTkFrame(
            master=self,
            fg_color="#1c1e1f",
            border_color="#1c1e1f",
            border_width=4,
            corner_radius=16, # UNDECIDED VISUAL CHANGE (rounded area or no)
            width=285,    # width
            height=380    # height
        )
        presetFrame.place(x=10, y=108)

        self.preset_list = ctk.CTkScrollableFrame(
            master=self, 
            width=260, 
            height=338,
            corner_radius=0,
            fg_color="#1c1e1f" 
        )

        self.preset_list.place(x=14, y=144)

        for preset in self.preset_manager.list_presets():
            btn = ctk.CTkButton(
                master=self.preset_list,
                text=preset,
                command=lambda name=preset: self._on_preset_select(name),
                width=254,  # full width of scrollable area
                anchor="w",  # align text to the left (optional)
                fg_color="#2a2a2a",
                text_color="#cbcbcb",
                font=("Arial", 16, "bold"),
                hover_color = "#303030",
                corner_radius = 4
            )
            btn.pack(pady=2)

            self.preset_buttons[preset] = btn

    #"""PRESET HEADER"""

        # Header Label
        header_frame = ctk.CTkFrame(  # Changed from CTkLabel to CTkFrame
            master=presetFrame,
            fg_color="#1c1e1f",
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
            text_color="#c4f04d",  # Dark text for contrast
            anchor="w",  # Left-aligned
            fg_color="transparent",  # Transparent background
            height=30
        )
        header_text.place(x=10, y=0)  # 10px left padding

    #"""PRESET BUTTONS"""

        folder_plus_path = os.path.join(script_dir, "images", "folder-plus-g.png")
        folder_plus_img = CTkImage(Image.open(folder_plus_path), size=(24, 24))

        # Plus button (placed absolutely)
        preset_plus_btn = ctk.CTkButton(
            master=header_frame,
            image=folder_plus_img,
            text="",
            text_color="#303030",
            font=("Arial", 18, "bold"),
            width=24,
            height=24,
            fg_color="transparent",
            hover_color="#2a2a2a",
            # corner_radius = 32, # CIRCULAR BUTTONS? WITH BORDERS?
            command=self._new_preset
        )
        # Place it at vertical center, near the right edge
        preset_plus_btn.place(relx=1.0, rely=0.5, x=-50, anchor="e")

        trash_path = os.path.join(script_dir, "images", "trash.png")
        trash_img = CTkImage(Image.open(trash_path), size=(24, 24))

        # Minus button (placed absolutely)
        preset_minus_btn = ctk.CTkButton(
            master=header_frame,
            image=trash_img,
            text="",
            text_color="#303030",
            font=("Arial", 18, "bold"),
            width=24,
            height=24,
            fg_color="transparent",
            hover_color="#2a2a2a",
            command=self._remove_preset
        )
        # Place it to the left of plus button, also centered vertically
        preset_minus_btn.place(relx=1.0, rely=0.5, x=-7, anchor="e")


#"""SCRIPTS SECTION"""

    #"""SCRIPTS FRAME"""
        # Right Frame (Scripts) - positioned to the right of presetFrame
        scriptsFrame = ctk.CTkFrame(
            master=self,
            fg_color="#1c1e1f",
            border_color="#1c1e1f",
            border_width=4,
            corner_radius=16, # UNDECIDED VISUAL CHANGE (rounded area or no)
            width=285,    # width
            height=380    # height
        )
        scriptsFrame.place(x=10 + 285 + 10, y=108)  # 10px gap from presetFrame

        self.scripts_list = ctk.CTkScrollableFrame(
            master=self, 
            width=260, 
            height=338,
            corner_radius=0,
            fg_color="#1c1e1f" 
        )

        self.scripts_list.place(x=309, y=144)

    #"""SCRIPTS HEADER"""

        # Header Label
        scripts_header_frame = ctk.CTkFrame(  # Changed from CTkLabel to CTkFrame
            master=scriptsFrame,
            fg_color="#1c1e1f",
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
            text_color="#c4f04d",  # Dark text for contrast
            anchor="w",  # Left-aligned
            fg_color="transparent",  # Transparent background
            height=30
        )
        scripts_header_text.place(x=10, y=0)  # 10px left padding

    #"""SCRIPTS BUTTONS"""

        file_plus_path = os.path.join(script_dir, "images", "file-plus.png")
        file_plus_img = CTkImage(Image.open(file_plus_path), size=(24, 24))

        # Plus button (placed absolutely)
        scripts_plus_btn = ctk.CTkButton(
            master=scripts_header_frame,
            image=file_plus_img,
            text="",
            text_color="#2C0735",
            font=("Arial", 18, "bold"),
            width=24,
            height=24,
            fg_color="transparent",
            hover_color="#2a2a2a",
            # corner_radius = 32, # CIRCULAR BUTTONS? WITH BORDERS?
            command=lambda: self._add_script_to_preset(self.current_preset)
        )
        # Place it at vertical center, near the right edge
        scripts_plus_btn.place(relx=1.0, rely=0.5, x=-50, anchor="e")

        # Minus button (placed absolutely)
        scripts_minus_btn = ctk.CTkButton(
            master=scripts_header_frame,
            image=trash_img,
            text="",
            text_color="#2C0735",
            font=("Arial", 18, "bold"),
            width=24,
            height=24,
            fg_color="transparent",
            hover_color="#2a2a2a",
            command=lambda: self._remove_script()
        )
        # Place it to the left of plus button, also centered vertically
        scripts_minus_btn.place(relx=1.0, rely=0.5, x=-7, anchor="e")


#"""OVERLAYS SECTION"""
    """
    #OVERLAYS FRAME
        # Right Frame (Scripts) - positioned to the right of presetFrame
        overlaysFrame = ctk.CTkFrame(
            master=self,
            fg_color="#090d0d",
            border_color="#613DC1",
            border_width=4,
            corner_radius=0, # STILL UNDECIDED VISUAL CHANGE
            width=285,
            height=185
        )
        overlaysFrame.place(x=10+285+10, y=110 + 110 + 30 + 10 + 10 + 10 + 10 + 10 + 5)  # 10px gap from presetFrame and below scriptsFram

    #OVERLAYS HEADER
        overlays_header_frame = ctk.CTkFrame(  # Changed from CTkLabel to CTkFrame
            master=overlaysFrame,
            fg_color="#858AE3",
            corner_radius=0,
            height=30,
            width = -8
        )
        overlays_header_frame.place(x=4, y=4, relwidth=0.97)

        # Header Text Label (added first so buttons appear on top)
        overlays_header_text = ctk.CTkLabel(
            master=overlays_header_frame,
            text="Overlays",
            font=("Arial", 16, "bold"),
            text_color="#2C0735",  # Dark text for contrast
            anchor="w",  # Left-aligned
            fg_color="transparent",  # Transparent background
            height=30
        )
        overlays_header_text.place(x=10, y=0)  # 10px left padding

    #SCRIPTS BUTTONS

        # Plus button (placed absolutely)
        overlays_plus_btn = ctk.CTkButton(
            master=overlays_header_frame,
            text="+",
            text_color="#2C0735",
            font=("Arial", 18, "bold"),
            width=20,
            height=20,
            fg_color="transparent",
            hover_color="#613DC1",
            # corner_radius = 32, # CIRCULAR BUTTONS? WITH BORDERS?
            # command=self.add_preset
        )
        # Place it at vertical center, near the right edge
        overlays_plus_btn.place(relx=1.0, rely=0.5, x=-32, anchor="e")

        # Minus button (placed absolutely)
        overlays_minus_btn = ctk.CTkButton(
            master=overlays_header_frame,
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
        overlays_minus_btn.place(relx=1.0, rely=0.5, x=-2, anchor="e")
    """

#"""COOLDOWNS SECTION"""


        # Right Frame (Scripts) - positioned to the right of presetFrame
    """
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
    """


#"""METHODS - probably need their own files in backend section"""

    def _new_preset(self):
        """Create new preset dialog with custom layout"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("New Preset")
        dialog.geometry("300x150")
        dialog.grab_set()  # Make dialog modal
        
        label = ctk.CTkLabel(dialog, text="Preset Name:")
        label.pack(pady=10)
        
        name_entry = ctk.CTkEntry(dialog)
        name_entry.pack(pady=10)
        
        def save_handler():
            name = name_entry.get()
            #print(name)
            if name:
                try:
                    self.preset_manager.save_preset(name, scripts=[])
                    #print("PRESET IS SAVED CORRECTLY")
                    self._refresh_presets()
                    #print("PRESETS GET REFRESHED")
                    dialog.destroy()
                    #print("DIALOG GETS DESTROYED")
                except Exception as e:
                    # Use CTkMessagebox for errors
                    #print("NOT ADDING TO CURRENT LIST?")
                    """
                    CTkMessagebox(
                        title="Error",
                        message=f"Failed to save preset: {str(e)}",
                        icon="cancel"
                    )
                    """
        
        save_btn = ctk.CTkButton(dialog, text="Save", command=save_handler)
        save_btn.pack(pady=10)

        for name, btn in self.preset_buttons.items():
            if name == self.current_preset:
                # Selected preset button (highlight)
                btn.configure(fg_color="#c4f04d", text_color="#171d18", hover_color = "#c4f04d")
            else:
                # Default button style
                btn.configure(fg_color="#2a2a2a", text_color="#cbcbcb", hover_color = "#303030")

    def _remove_preset(self):
        """Removes the currently selected preset"""
        if not self.current_preset:
            CTkMessagebox(
                title="No Preset Selected",
                message="Please select a preset to remove.",
                icon="warning"
            )
            return

        confirm = CTkMessagebox(
            title="Confirm Delete",
            message=f"Are you sure you want to delete the preset '{self.current_preset}'?",
            icon="question",
            option_1="Yes",
            option_2="Cancel"
        )

        if confirm.get() == "Yes":
            try:
                self.preset_manager.delete_preset(self.current_preset)
                self.current_preset = None
                self._refresh_presets()
            except Exception as e:
                CTkMessagebox(
                    title="Error",
                    message=f"Failed to delete preset: {str(e)}",
                    icon="cancel"
                )

        for name, btn in self.preset_buttons.items():
            btn.configure(fg_color="#2a2a2a", text_color="#cbcbcb", hover_color = "#303030")

    def _refresh_presets(self):
        """Reload presets from disk and update the dropdown"""
        preset_names = self.preset_manager.list_presets()
        #print(preset_names) # SUCCESSFULLY PRINTS THE ADDED PRESET 

        self.preset_buttons = {}

        # Clear existing preset buttons
        for widget in self.preset_list.winfo_children():
            widget.destroy()

        # Add new buttons for each preset
        for preset in preset_names:
            btn = ctk.CTkButton(
                master=self.preset_list,
                text=preset,
                command=lambda name=preset: self._on_preset_select(name),
                width=254,  # full width of scrollable area
                anchor="w",  # align text to the left (optional)
                fg_color="#2a2a2a",
                text_color="#cbcbcb",
                font=("Arial", 16, "bold"),
                corner_radius=16
            )
            btn.pack(pady=2)
            self.preset_buttons[preset] = btn

        if self.current_preset in self.preset_buttons:
            self._on_preset_select(self.current_preset)

    def _on_preset_select(self, preset_name):
        """Handle user selection from the presets list"""
        previous_selected = self.current_preset
        self.current_preset = preset_name
        #print(f"{preset_name} selected (Previous was {previous_selected})")
        self._refresh_scripts(preset_name)

            
        for name, btn in self.preset_buttons.items():
            if name == preset_name:
                if name == previous_selected:
                    btn.configure(fg_color="#2a2a2a", text_color="#cbcbcb", hover_color = "#303030")
                    self.current_preset = None
                    self._refresh_scripts(self.current_preset)
                else:
                    # Selected preset button (highlight)
                    btn.configure(fg_color="#c4f04d", text_color="#171d18", hover_color = "#c4f04d")
            else:
                # Default button style
                btn.configure(fg_color="#2a2a2a", text_color="#cbcbcb", hover_color = "#303030")

        #print(f"Selected preset: {preset_name}")

    def _add_script_to_preset(self, preset_name):
        """Open file explorer to add a .ahk script to the preset"""
        # Open file explorer to choose a script
        script_path = filedialog.askopenfilename(
            title="Select Script File", 
            filetypes=(("AutoHotkey Scripts", "*.ahk"), ("All Files", "*.*"))
        )

        if script_path:  # Only proceed if the user selected a file
            script_name = script_path.split('/')[-1]  # Extract the file name from the path
            try:
                # Add the selected script to the preset
                self.preset_manager.add_script_to_preset(preset_name, script_name)
                self._refresh_scripts(preset_name)  # Refresh the script list
            except Exception as e:
                ctk.CTkMessagebox(
                    title="Error",
                    message=f"Failed to add script: {str(e)}",
                    icon="cancel"
                )

    def _refresh_scripts(self, preset_name):
        """Reload and display scripts for the selected preset"""
        script_names = self.preset_manager.list_scripts(preset_name)

        self.script_buttons = {}

        # Clear existing script buttons
        for widget in self.scripts_list.winfo_children():
            widget.destroy()

        # Add new buttons for each script
        for script in script_names:
            btn = ctk.CTkButton(
                master=self.scripts_list,
                text=script,
                command=lambda name=script: self._on_script_select(name),
                width=254,  # full width of scrollable area
                anchor="w",  # align text to the left (optional)
                fg_color="#2a2a2a",
                hover_color="#303030",
                text_color="#cbcbcb",
                font=("Arial", 16, "bold"),
                corner_radius=4

            )
            btn.pack(pady=2)

            self.script_buttons[script] = btn

        #if self.current_script in self.script_buttons:
        #    self._on_script_select(self.current_script)

    def _on_script_select(self, script_name):
        """Handles script selection action"""
        previous_script = self.current_script
        self.current_script = script_name
        #print(f"{script_name} selected. (Previous script was {previous_script})")

        selected_btn = self.script_buttons.get(script_name)

        # Update the color of the previously selected script (if any)
        if self.current_script is not None:
            prev_selected_btn = self.script_buttons.get(previous_script)
            if prev_selected_btn:
                prev_selected_btn.configure(fg_color="#2a2a2a", text_color="#cbcbcb", hover_color="#303030")  # Reset to default color

        # Update the color of the newly selected script
        if selected_btn:
            if previous_script == script_name:
                selected_btn.configure(fg_color="#2a2a2a")
                self.current_script = None
            else:
                selected_btn.configure(fg_color="#c4f04d", text_color="#171d18", hover_color="#c4f04d")  # Highlight color for selected script

        # Update the currently selected script tracker

        #print(f"Script selected: {script_name}")
        # Add your script running logic here

    def _remove_script(self):
        """Removes the currently selected script"""
        if not self.current_script:
            CTkMessagebox(
                title="No Preset Selected",
                message="Please select a preset to remove.",
                icon="warning"
            )
            return

        confirm = CTkMessagebox(
            title="Confirm Delete",
            message=f"Are you sure you want to delete the script '{self.current_script}' in '{self.current_preset}'?",
            icon="question",
            option_1="Yes",
            option_2="Cancel"
        )

        if confirm.get() == "Yes":
            try:
                self.preset_manager.delete_script(self.current_script)
                self.current_script = None
                self._refresh_scripts()
            except Exception as e:
                CTkMessagebox(
                    title="Error",
                    message=f"Failed to delete script: {str(e)}",
                    icon="cancel"
                )

        for name, btn in self.script_buttons.items():
            btn.configure(fg_color="#2a2a2a", text_color="#cbcbcb", hover_color = "#303030")

if __name__ == "__main__":
    app = LineagePlusApp()
    app.mainloop()
