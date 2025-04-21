import customtkinter as ctk
from customtkinter import CTkImage
from CTkMessagebox import CTkMessagebox # pip install CTkMessagebox
import tkinter.filedialog as filedialog
from tkinter import PhotoImage
from PIL import Image # pip install pillow
from backend.preset_manager import PresetManager
from backend.script_runner import ScriptRunner
from backend.utils import ToolTip
from frontend.about import AboutPage
import os

# Set appearance mode and default color theme
ctk.set_appearance_mode("dark")
#ctk.set_default_color_theme("blue")

class LineagePlusApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        script_dir = os.path.dirname(__file__)
        icon_path = os.path.join(script_dir, "images", "white_plus.ico")  # Must be .ico

        if os.path.exists(icon_path):
            self.after(201, lambda: self.iconbitmap(icon_path))
        else:
            print(f"Icon file not found: {icon_path}")

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
        self.geometry("600x500") #original build - 600x500
        self.resizable(False, False)

        self.page_container = ctk.CTkFrame(master=self, fg_color="transparent")
        self.page_container.place(relx=0, rely=0, relwidth=1, relheight=1)

        self.main_page = LineagePlusApp


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
                size=(208, 44)  # Adjust size as needed
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
        header_container.pack(side="top", fill="x", padx=30, pady=20)  # Automatic width

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

        run_button_path = os.path.join(script_dir, "images", "play.png")
        run_button_img = CTkImage(Image.open(run_button_path), size=(24, 24))

        # run button (placed absolutely)
        run_btn = ctk.CTkButton(
            master=header_container,
            text="",
            text_color="#858AE3",
            image=run_button_img,
            font=("Arial", 18, "bold"),
            width=24,
            height=24,
            fg_color="transparent",
            hover_color="#2a2a2a",
            corner_radius=4,
            # corner_radius = 32, # CIRCULAR BUTTONS? WITH BORDERS?
            command=lambda: self._run_preset_scripts()
        )
        # Place it at vertical center, near the right edge
        run_btn.place(relx=1.0, rely=0.5, x=-122, anchor="e")
        ToolTip(run_btn, "Run")

        stop_button_path = os.path.join(script_dir, "images", "stop.png")
        stop_button_img = CTkImage(Image.open(stop_button_path), size=(24, 24))

        # stop button (placed absolutely)
        stop_btn = ctk.CTkButton(
            master=header_container,
            text="",
            text_color="#858AE3",
            image=stop_button_img,
            font=("Arial", 18, "bold"),
            width=24,
            height=24,
            fg_color="transparent",
            hover_color="#2a2a2a",
            corner_radius = 4,
            command=lambda: self._stop_current_scripts()
        )
        # Place it to the left of plus button, also centered vertically
        stop_btn.place(relx=1.0, rely=0.5, x=-62, anchor="e")
        ToolTip(stop_btn, "Stop")

        at_sign_path = os.path.join(script_dir, "images", "at-sign.png")
        at_button_img = CTkImage(Image.open(at_sign_path), size=(24, 24))

        # about button (placed absolutely)
        at_btn = ctk.CTkButton(
            master=header_container,
            text="",
            text_color="#858AE3",
            image=at_button_img,
            font=("Arial", 18, "bold"),
            width=24,
            height=24,
            fg_color="transparent",
            hover_color="#2a2a2a",
            corner_radius = 4,
            command=self.show_about  
        )
        # Place it to the left of plus button, also centered vertically
        at_btn.place(relx=1.0, rely=0.5, x=-2, anchor="e")
        ToolTip(at_btn, "About")

#"""PRESETS SECTION"""

    #"""PRESET FRAME"""


        presetFrame = ctk.CTkFrame(
            master=self,
            fg_color="#1c1e1f",
            border_color="#1c1e1f",
            border_width=4,
            corner_radius=8, # UNDECIDED VISUAL CHANGE (rounded area or no)
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
        # self.preset_list._scrollbar.grid_forget()  # Hide the scrollbar

        # (Idea for side scroll bar currently opting to just hide it)
        self.preset_list._scrollbar.configure(
            fg_color="#1c1e1f",
            button_color="#2a2a2a",
            button_hover_color="#303030"
        )
        
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
        ToolTip(preset_plus_btn, "+ Preset")

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
        ToolTip(preset_minus_btn, "- Preset")

#"""SCRIPTS SECTION"""

    #"""SCRIPTS FRAME"""
        # Right Frame (Scripts) - positioned to the right of presetFrame
        scriptsFrame = ctk.CTkFrame(
            master=self,
            fg_color="#1c1e1f",
            border_color="#1c1e1f",
            border_width=4,
            corner_radius=8, # UNDECIDED VISUAL CHANGE (rounded area or no)
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

        self.scripts_list._scrollbar.configure(
            fg_color="#1c1e1f",
            button_color="#2a2a2a",
            button_hover_color="#303030"
        )        

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
        ToolTip(scripts_plus_btn, "+ Script")

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
        ToolTip(scripts_minus_btn, "- Script")

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
                    self.current_preset = name  # Set the newly created preset as current
                    self._refresh_presets()
                    self._on_preset_select(name)
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
                self.current_script = None
                self._refresh_presets()
                self._refresh_scripts(None) 
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
                corner_radius=4
            )
            btn.pack(pady=2)
            self.preset_buttons[preset] = btn

        if self.current_preset in self.preset_buttons:
            self._on_preset_select(self.current_preset)

    def _on_preset_select(self, preset_name):
        """Handle user selection from the presets list"""
        previous_selected = self.current_preset
        self.current_preset = preset_name
        self.current_script = None
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
        if self.current_preset != None:
            script_path = filedialog.askopenfilename(
                title="Select Script File", 
                filetypes=(("AutoHotkey Scripts", "*.ahk"), ("All Files", "*.*"))
            )

            if script_path:  # Only proceed if the user selected a file
                try:
                    # Pass the full path to the preset manager
                    self.preset_manager.add_script_to_preset(preset_name, script_path)
                    self._refresh_scripts(preset_name)  # Refresh the script list
                except Exception as e:
                    ctk.CTkMessagebox(
                        title="Error",
                        message=f"Failed to add script: {str(e)}",
                        icon="cancel"
                    )

        else:
            CTkMessagebox(
                title="No Preset Selected",
                message="Please select a preset first.",
                icon="warning"
            )
            #print("No preset selected. Select a preset first")


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
                message="Please select a script to remove.",
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
                self.preset_manager.remove_script_from_preset(self.current_preset, self.current_script)
                self.current_script = None
                self._refresh_scripts(self.current_preset)
            except Exception as e:
                CTkMessagebox(
                    title="Error",
                    message=f"Failed to delete script: {str(e)}",
                    icon="cancel"
                )

        for name, btn in self.script_buttons.items():
            btn.configure(fg_color="#2a2a2a", text_color="#cbcbcb", hover_color = "#303030")


    def _run_preset_scripts(self):
        if not self.current_preset:
            CTkMessagebox(
                title="No Preset Selected",
                message="Please select a preset before running.",
                icon="warning"
            )
            return

        scripts = self.preset_manager.list_scripts(self.current_preset)
        script_dir = self.preset_manager.scripts_dir

        errors = self.script_runner.run_scripts(scripts, script_dir)

        if errors:
            error_messages = "\n".join(f"{name}: {msg}" for name, msg in errors)
            CTkMessagebox(
                title="Script Errors",
                message=error_messages,
                icon="cancel"
            )

    def _stop_current_scripts(self):
        stopped = self.script_runner.stop_scripts()

        if stopped:
            msg = "Stopped the following script(s):\n" + "\n".join(stopped)
            icon = "check"
        else:
            msg = "No running AHK scripts found to stop."
            icon = "warning"

        CTkMessagebox(
            title="Script Stop Result",
            message=msg,
            icon=icon
        )

    def show_about(self):
        # create the AboutPage as a full-window overlay
        self.about_page = AboutPage(
            master=self,                  # parent is your root window
            close_callback=self.close_about
        )
        # stretch it over the entire window
        self.about_page.place(relx=0, rely=0, relwidth=1, relheight=1)

    def close_about(self):
        # destroy the overlay and all its children
        if hasattr(self, "about_page"):
            self.about_page.destroy()
            del self.about_page


if __name__ == "__main__":
    app = LineagePlusApp()
    app.mainloop()
