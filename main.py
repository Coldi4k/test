import keyboard
import tkinter as tk
import subprocess
import time
import pystray
from PIL import Image, ImageDraw
import threading

class OverlayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Overlay")
        self.root.attributes("-fullscreen", True)
        self.root.attributes("-topmost", True)
        self.root.attributes("-alpha", 0.9)  # More transparent background
        self.root.overrideredirect(True)  # Remove window borders

        # Create a frame for the overlay content
        self.frame = tk.Frame(root, bg="#000000", bd=2)
        self.frame.pack(fill=tk.BOTH, expand=True)

        # Title bar
        self.title_bar = tk.Label(self.frame, text="Magic Help", bg="#000000", fg="white", font=("Arial", 16, "bold"))
        self.title_bar.pack()

        # Close button
        self.close_button = tk.Button(self.frame, text="X", command=self.hide_overlay, bg="#2f2f2f", fg="white", font=("Arial", 12, "bold"), relief=tk.FLAT, width=2, height=1, activebackground="#2f2f2f", activeforeground="white")
        self.close_button.place(relx=1.0, rely=0.0, anchor="ne", x=-25, y=25)

        # Clock
        self.clock_label = tk.Label(self.frame, bg="#000000", fg="white", font=("Arial", 20, "bold"))  # Increased font size
        self.clock_label.place(relx=0.0, rely=0.0, anchor="nw", x=25, y=25)
        self.date_label = tk.Label(self.frame, bg="#000000", fg="white", font=("Arial", 12, "bold"))  # Date label
        self.date_label.place(relx=0.0, rely=0.0, anchor="nw", x=25, y=60)
        self.update_clock()

        # Crosshair button
        self.crosshair_button = tk.Canvas(self.frame, bg="#2f2f2f", width=40, height=40, highlightthickness=0)  # Dark gray background
        self.crosshair_button.create_line(20, 10, 20, 30, fill="white", width=2)
        self.crosshair_button.create_line(10, 20, 30, 20, fill="white", width=2)
        self.crosshair_button.place(relx=0.5, rely=1.0, anchor="s", y=-40)
        self.crosshair_button.bind("<Button-1>", self.toggle_crosshair)

        self.crosshair_process = None
        self.root.withdraw()  # Hide the window initially

        # Create system tray icon
        self.create_tray_icon()

    def toggle_crosshair(self, event=None):
        if self.crosshair_process is None:
            self.crosshair_button.config(bg="#07bdf5")  # Change to light blue when active
            self.crosshair_process = subprocess.Popen(["python", "crosshair.py"])
        else:
            self.crosshair_button.config(bg="#2f2f2f")  # Change back to dark gray when inactive
            self.crosshair_process.terminate()
            self.crosshair_process = None

    def show_overlay(self):
        self.root.deiconify()

    def hide_overlay(self):
        self.root.withdraw()

    def close_overlay(self):
        if self.crosshair_process:
            self.crosshair_process.terminate()
        self.tray_icon.stop()
        self.root.quit()

    def update_clock(self):
        current_time = time.strftime("%I:%M %p")  # 12-hour format with AM/PM
        current_date = time.strftime("%a, %B %d, %Y")  # Date format like "Tue, August 25, 2023"
        self.clock_label.config(text=current_time)
        self.date_label.config(text=current_date)
        self.root.after(1000, self.update_clock)

    def create_tray_icon(self):
        icon_image = Image.open("icon.png")

        # Define the menu
        menu = pystray.Menu(
            pystray.MenuItem('Open', self.show_overlay),  # Add Open button
            pystray.MenuItem('Close', self.close_overlay)
        )

        # Create the tray icon
        self.tray_icon = pystray.Icon("Magic Help", icon_image, "Magic Help", menu)

        # Run the tray icon in a separate thread
        threading.Thread(target=self.tray_icon.run).start()

def main():
    root = tk.Tk()
    app = OverlayApp(root)

    def on_hotkey():
        if app.root.state() == "withdrawn":
            app.show_overlay()
        else:
            app.hide_overlay()

    keyboard.add_hotkey("ctrl+shift+tab", on_hotkey)

    root.mainloop()

if __name__ == "__main__":
    main()
