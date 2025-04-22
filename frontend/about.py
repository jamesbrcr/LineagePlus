import customtkinter as ctk
import requests
from PIL import Image # pip install pillow
from customtkinter import CTkImage
from backend.utils import ToolTip
import os

class AboutPage(ctk.CTkFrame):
    def __init__(self, master, close_callback=None, **kwargs):
        self.close_callback = close_callback
        super().__init__(master, **kwargs)

        self.configure(fg_color="#1c1e1f")

        script_dir = os.path.dirname(__file__)

        header_container = ctk.CTkFrame(
            master=self,
            fg_color="#1c1e1f",
            height=100  # Match your title image height
        )
        header_container.pack(side="top", fill="x", padx=30, pady=(5, 0))  # Less top space

        #SCROOM IMAGE
        scroom_path = os.path.join(script_dir, "images", "scroom.png")
        scroom_img = CTkImage(Image.open(scroom_path), size=(210, 262))
        scroom_label = ctk.CTkLabel(master=self, image=scroom_img, text="")
        scroom_label.place(x=-10, y=270)

        #SILVER IMAGE
        silver_path = os.path.join(script_dir, "images", "silver.png")
        silver_img = CTkImage(Image.open(silver_path), size=(50, 50))
        silver_label = ctk.CTkLabel(master=self, image=silver_img, text="")
        silver_label.place(x=455, y=220)

        #SOCIALS BUTTON
        socials_btn = ctk.CTkButton(
            self, 
            text="Follow Me", 
            text_color="#c4f04d",
            font=("Arial", 18, "bold"),
            width=110,
            height=36,
            fg_color="#303030",
            hover_color="#2a2a2a",
            corner_radius = 16,
            command=self._open_site
        )
        socials_btn.place(x=150, y=310)

        #SUPPORT BUTTON
        support_btn = ctk.CTkButton(
            master=self,
            text="Support",
            text_color="#c4f04d",
            font=("Arial", 18, "bold"),
            width=110,
            height=36,
            fg_color="#303030",
            hover_color="#2a2a2a",
            corner_radius = 16,
            command=self._open_support_link
        )
        support_btn.place(x=350, y=229)

        #DOWNLOADS AND VERSION TEXT
        downloads = self.get_download_count()
        downloads_label = ctk.CTkLabel(
            self,
            text=f"Version 1.0.1    |    {downloads} Downloads",
            text_color="#cbcbcb",
            font=("Arial", 16),
        )
        downloads_label.place(relx=0.5, rely=0.99, anchor="s")

        home_path = os.path.join(script_dir, "images", "home-2.png")
        home_img = CTkImage(Image.open(home_path), size=(24, 24))

        title_path = os.path.join(script_dir, "images", "healer_icon.png")
        title_img = CTkImage(Image.open(title_path), size=(130, 130))

        # TITLE IMAGE
        title_image_label = ctk.CTkLabel(
            master=header_container,
            image=title_img,
            text=""
        )
        title_image_label.pack(side="top")

        # home button (placed absolutely)
        home_btn = ctk.CTkButton(
            master=self,
            text="Return",
            text_color="#c4f04d",
            image=home_img,
            font=("Arial", 18, "bold"),
            width=130,
            height=36,
            fg_color="#303030",
            hover_color="#2a2a2a",
            corner_radius = 16,
            command=self.close_callback
        )
        home_btn.place(relx=0.5, y=120, anchor="n")

    def _open_support_link(self):
        import webbrowser
        webbrowser.open("https://buymeacoffee.com/jamesbrcr")

    def _open_site(self):
        import webbrowser
        webbrowser.open("https://james-crowe-dev.vercel.app/")

    def get_download_count(self):
        try:
            response = requests.get("https://api.github.com/repos/jamesbrcr/LineagePlus/releases/latest")
            data = response.json()
            assets = data.get("assets", [])
            return sum(asset.get("download_count", 0) for asset in assets)
        except Exception as e:
            print(f"Error fetching download count: {e}")
            return "N/A"