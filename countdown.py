import tkinter as tk                                      # Creates the graphical interface
from pathlib import Path                                  # Creates reliable file paths
from PIL import Image, ImageTk                            # Opens and displays images

IMAGE_FOLDER = Path(__file__).parent / "countdown_images" # Folder holding countdown0.jpg ... countdown30.jpg
GAME_START_SECONDS = 30                                   # Length of the pre-game countdown


class CountdownTimer:                                     # Shows the pre-game countdown over the window

    def __init__(self, parent, on_complete, seconds=GAME_START_SECONDS, on_cancel=None):
        self.parent = parent                              # Window or frame the countdown covers
        self.on_complete = on_complete                    # Called when the countdown reaches 0
        self.on_cancel = on_cancel                        # Called if the countdown is cancelled
        self.seconds_left = seconds                       # Seconds remaining
        self.after_id = None                              # Pending tick, so it can be cancelled
        self.running = False                              # True while the countdown is on screen
        self.photo = None                                 # Keeps the current image from being garbage collected

        self.frame = tk.Frame(parent, bg="black")         # Black panel that covers the parent
        self.label = tk.Label(
            self.frame,                                   # Places the label in the countdown panel
            bg="black",                                   # Matches the panel background
            fg="#ffd700",                                 # Gold text for the fallback number
            font=("Arial", 160, "bold")                   # Large font for the fallback number
        )
        self.label.pack(expand=True, fill="both")         # Centers the image or number

    def start(self):                                      # Shows the countdown and starts ticking
        if self.running:                                  # Ignores repeat starts (F5 pressed twice)
            return
        self.running = True
        self.frame.place(relx=0, rely=0, relwidth=1, relheight=1)  # Covers the whole parent
        self.frame.lift()                                 # Draws on top of the entry screen
        self.parent.update_idletasks()                    # Gets the real window size for image scaling
        self.tick()

    def tick(self):                                       # Runs once per second
        self.show_number(self.seconds_left)
        if self.seconds_left <= 0:                        # Countdown finished
            self.after_id = self.parent.after(500, self.finish)  # Holds on 0 briefly, then starts
            return
        self.seconds_left -= 1
        self.after_id = self.parent.after(1000, self.tick)

    def show_number(self, number):                        # Displays the image for one number
        image_path = IMAGE_FOLDER / f"countdown{number}.jpg"
        try:
            image = Image.open(image_path)                # Opens the countdown image
            width = max(self.frame.winfo_width(), 400)    # Current panel width
            height = max(self.frame.winfo_height(), 300)  # Current panel height
            image.thumbnail((width, height))              # Scales to fit while keeping proportions
            self.photo = ImageTk.PhotoImage(image)        # Converts the image for Tkinter
            self.label.config(image=self.photo, text="")
        except (OSError, FileNotFoundError):              # Falls back to plain text if the image is missing
            self.photo = None
            self.label.config(image="", text=str(number))

    def finish(self):                                     # Removes the countdown and hands off to the game
        self.stop()
        self.on_complete()

    def cancel(self):                                     # Stops early without starting the game
        if not self.running:
            return
        self.stop()
        if self.on_cancel:
            self.on_cancel()

    def stop(self):                                       # Cancels the pending tick and hides the panel
        if self.after_id is not None:
            self.parent.after_cancel(self.after_id)
            self.after_id = None
        self.running = False
        if self.frame.winfo_exists():
            self.frame.destroy()
