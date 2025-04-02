# dependencies because I am lazy and cannot be bothered...
# brew install python-tk
# brew install tcl-tk
# pip install pillow (if I add images for the presets)

from frontend.app import LineagePlusApp

if __name__ == "__main__":
    app = LineagePlusApp()
    app.mainloop()