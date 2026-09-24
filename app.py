import tkinter as tk                                      # Creates the graphical interface
from tkinter import messagebox                            # Creates popup messages
from pathlib import Path                                 # Creates reliable file paths
from PIL import Image, ImageTk                           # Opens and displays images


class LaserTagApp:                                       # Controls the laser tag application

    def __init__(self, root):                            # Runs when the application is created
        self.root = root                                 # Stores the main application window
        self.root.title("Photon Laser Tag")              # Sets the window title
        self.root.geometry("1000x700")                   # Sets the window size
        self.root.configure(bg="black")                  # Sets the starting background color

        self.red_players = []                            # Stores red team players
        self.green_players = []                          # Stores green team players

        self.root.bind("<F5>", self.start_game)          # Connects F5 to the Start Game function
        self.root.bind("<F12>", self.clear_all_players)  # Connects F12 to the Clear All function

        self.show_splash_screen()                        # Displays the splash screen first


    def clear_screen(self):                              # Removes everything from the current screen
        for widget in self.root.winfo_children():        # Gets every widget in the window
            widget.destroy()                             # Removes the current widget


    def show_splash_screen(self):                        # Creates the splash screen
        self.clear_screen()                              # Removes widgets from the previous screen
        self.root.configure(bg="black")                  # Sets the splash background to black

        app_folder = Path(__file__).parent               # Gets the folder containing app.py
        logo_path = app_folder / "logo.jpg"              # Creates the path to logo.jpg

        logo = Image.open(logo_path)                     # Opens the logo image
        logo.thumbnail((900, 600))                       # Resizes the logo while keeping its proportions

        self.logo_image = ImageTk.PhotoImage(logo)       # Converts the image for Tkinter

        logo_label = tk.Label(
            self.root,                                   # Places the label in the main window
            image=self.logo_image,                       # Displays the logo
            bg="black"                                   # Matches the splash background
        )

        logo_label.pack(expand=True)                     # Centers the logo in the window

        self.root.after(
            3000,                                        # Waits 3000 milliseconds
            self.show_player_entry                       # Opens the player entry screen
        )


    def show_player_entry(self):                         # Creates the player entry screen
        self.clear_screen()                              # Removes the splash screen
        self.root.configure(bg="#171717")                # Sets the player entry background

        heading = tk.Label(
            self.root,                                   # Places the heading in the main window
            text="Photon Laser Tag - Player Entry",      # Sets the heading text
            font=("Arial", 26, "bold"),                  # Sets the heading font
            fg="white",                                  # Sets the heading text color
            bg="#171717"                                 # Matches the window background
        )

        heading.pack(pady=15)                            # Displays the heading with vertical spacing

        entry_frame = tk.Frame(
            self.root,                                   # Places the frame in the main window
            bg="#2b2b2b",                                # Sets the frame background
            padx=20,                                     # Adds horizontal spacing inside the frame
            pady=15                                      # Adds vertical spacing inside the frame
        )

        entry_frame.pack(
            fill="x",                                    # Stretches the frame horizontally
            padx=30                                      # Adds spacing around the frame
        )

        player_id_label = tk.Label(
            entry_frame,                                 # Places the label in the entry frame
            text="Player ID:",                           # Sets the label text
            font=("Arial", 12),                          # Sets the label font
            fg="white",                                  # Sets the label text color
            bg="#2b2b2b"                                 # Matches the entry frame background
        )

        player_id_label.grid(
            row=0,                                       # Places the label in row 0
            column=0,                                    # Places the label in column 0
            padx=5,                                      # Adds horizontal spacing
            pady=5                                       # Adds vertical spacing
        )

        self.player_id_entry = tk.Entry(
            entry_frame,                                 # Places the input inside the entry frame
            width=15,                                    # Sets the input width
            font=("Arial", 12)                           # Sets the input font
        )

        self.player_id_entry.grid(
            row=0,                                       # Places the input in row 0
            column=1,                                    # Places the input in column 1
            padx=5,                                      # Adds horizontal spacing
            pady=5                                       # Adds vertical spacing
        )

        codename_label = tk.Label(
            entry_frame,                                 # Places the label in the entry frame
            text="Codename:",                            # Sets the label text
            font=("Arial", 12),                          # Sets the label font
            fg="white",                                  # Sets the label text color
            bg="#2b2b2b"                                 # Matches the entry frame background
        )

        codename_label.grid(
            row=0,                                       # Places the label in row 0
            column=2,                                    # Places the label in column 2
            padx=5,                                      # Adds horizontal spacing
            pady=5                                       # Adds vertical spacing
        )

        self.codename_entry = tk.Entry(
            entry_frame,                                 # Places the input inside the entry frame
            width=18,                                    # Sets the input width
            font=("Arial", 12)                           # Sets the input font
        )

        self.codename_entry.grid(
            row=0,                                       # Places the input in row 0
            column=3,                                    # Places the input in column 3
            padx=5,                                      # Adds horizontal spacing
            pady=5                                       # Adds vertical spacing
        )

        equipment_id_label = tk.Label(
            entry_frame,                                 # Places the label in the entry frame
            text="Equipment ID:",                        # Sets the label text
            font=("Arial", 12),                          # Sets the label font
            fg="white",                                  # Sets the label text color
            bg="#2b2b2b"                                 # Matches the entry frame background
        )

        equipment_id_label.grid(
            row=0,                                       # Places the label in row 0
            column=4,                                    # Places the label in column 4
            padx=5,                                      # Adds horizontal spacing
            pady=5                                       # Adds vertical spacing
        )

        self.equipment_id_entry = tk.Entry(
            entry_frame,                                 # Places the input inside the entry frame
            width=15,                                    # Sets the input width
            font=("Arial", 12)                           # Sets the input font
        )

        self.equipment_id_entry.grid(
            row=0,                                       # Places the input in row 0
            column=5,                                    # Places the input in column 5
            padx=5,                                      # Adds horizontal spacing
            pady=5                                       # Adds vertical spacing
        )

        self.selected_team = tk.StringVar(value="red")   # Stores the selected team

        red_choice = tk.Radiobutton(
            entry_frame,                                 # Places the option in the entry frame
            text="Red Team",                             # Sets the option text
            variable=self.selected_team,                 # Stores the selection in selected_team
            value="red",                                 # Selects red when clicked
            font=("Arial", 11, "bold"),                  # Sets the option font
            fg="red",                                    # Sets the text color
            bg="#2b2b2b",                                # Matches the entry frame background
            selectcolor="#171717"                        # Sets the selected circle background
        )

        red_choice.grid(
            row=1,                                       # Places the option in row 1
            column=1,                                    # Places the option in column 1
            pady=8                                       # Adds vertical spacing
        )

        green_choice = tk.Radiobutton(
            entry_frame,                                 # Places the option in the entry frame
            text="Green Team",                           # Sets the option text
            variable=self.selected_team,                 # Stores the selection in selected_team
            value="green",                               # Selects green when clicked
            font=("Arial", 11, "bold"),                  # Sets the option font
            fg="#39ff14",                                # Sets the text color
            bg="#2b2b2b",                                # Matches the entry frame background
            selectcolor="#171717"                        # Sets the selected circle background
        )

        green_choice.grid(
            row=1,                                       # Places the option in row 1
            column=2,                                    # Places the option in column 2
            pady=8                                       # Adds vertical spacing
        )

        add_button = tk.Button(
            entry_frame,                                 # Places the button in the entry frame
            text="Add Player",                           # Sets the button text
            font=("Arial", 11, "bold"),                  # Sets the button font
            command=self.add_player                      # Calls add_player when clicked
        )

        add_button.grid(
            row=1,                                       # Places the button in row 1
            column=4,                                    # Places the button in column 4
            columnspan=2,                                # Uses two columns
            pady=8                                       # Adds vertical spacing
        )

        for column in range(6):                          # Loops through all six entry frame columns
            entry_frame.grid_columnconfigure(
                column,                                  # Selects the current column
                weight=1                                 # Allows the column to expand
            )

        teams_frame = tk.Frame(
            self.root,                                   # Places the frame in the main window
            bg="#171717"                                 # Matches the window background
        )

        teams_frame.pack(
            fill="both",                                 # Stretches the frame horizontally and vertically
            expand=True,                                 # Uses the remaining window space
            padx=30,                                     # Adds horizontal spacing
            pady=15                                      # Adds vertical spacing
        )

        red_frame = tk.Frame(
            teams_frame,                                 # Places the frame in the teams frame
            bg="#3b1111",                                # Sets the red team background
            padx=15,                                     # Adds horizontal spacing
            pady=10                                      # Adds vertical spacing
        )

        red_frame.pack(
            side="left",                                 # Places the red team on the left
            fill="both",                                 # Stretches the red frame
            expand=True,                                 # Uses available space
            padx=(0, 10)                                 # Adds spacing to the right
        )

        red_heading = tk.Label(
            red_frame,                                   # Places the heading in the red frame
            text="RED TEAM",                             # Sets the heading text
            font=("Arial", 20, "bold"),                  # Sets the heading font
            fg="white",                                  # Sets the heading text color
            bg="#3b1111"                                 # Matches the red frame background
        )

        red_heading.pack(pady=5)                         # Displays the red team heading

        self.red_listbox = tk.Listbox(
            red_frame,                                   # Places the list in the red frame
            height=15,                                   # Displays space for 15 players
            font=("Arial", 12),                          # Sets the list font
            bg="#fff0f0"                                 # Sets the list background
        )

        self.red_listbox.pack(
            fill="both",                                 # Stretches the list
            expand=True                                  # Uses the available red frame space
        )

        green_frame = tk.Frame(
            teams_frame,                                 # Places the frame in the teams frame
            bg="#113b1b",                                # Sets the green team background
            padx=15,                                     # Adds horizontal spacing
            pady=10                                      # Adds vertical spacing
        )

        green_frame.pack(
            side="right",                                # Places the green team on the right
            fill="both",                                 # Stretches the green frame
            expand=True,                                 # Uses available space
            padx=(10, 0)                                 # Adds spacing to the left
        )

        green_heading = tk.Label(
            green_frame,                                 # Places the heading in the green frame
            text="GREEN TEAM",                           # Sets the heading text
            font=("Arial", 20, "bold"),                  # Sets the heading font
            fg="white",                                  # Sets the heading text color
            bg="#113b1b"                                 # Matches the green frame background
        )

        green_heading.pack(pady=5)                       # Displays the green team heading

        self.green_listbox = tk.Listbox(
            green_frame,                                 # Places the list in the green frame
            height=15,                                   # Displays space for 15 players
            font=("Arial", 12),                          # Sets the list font
            bg="#effff1"                                 # Sets the list background
        )

        self.green_listbox.pack(
            fill="both",                                 # Stretches the list
            expand=True                                  # Uses the available green frame space
        )

        controls_frame = tk.Frame(
            self.root,                                   # Places the controls in the main window
            bg="#171717"                                 # Matches the window background
        )

        controls_frame.pack(pady=(0, 15))                # Displays the controls at the bottom

        clear_button = tk.Button(
            controls_frame,                              # Places the button in the controls frame
            text="Clear All (F12)",                      # Sets the button text
            font=("Arial", 12, "bold"),                  # Sets the button font
            command=self.clear_all_players               # Calls clear_all_players when clicked
        )

        clear_button.pack(
            side="left",                                 # Places the button on the left
            padx=10                                      # Adds horizontal spacing
        )

        start_button = tk.Button(
            controls_frame,                              # Places the button in the controls frame
            text="Start Game (F5)",                      # Sets the button text
            font=("Arial", 12, "bold"),                  # Sets the button font
            command=self.start_game                      # Calls start_game when clicked
        )

        start_button.pack(
            side="left",                                 # Places the button beside Clear All
            padx=10                                      # Adds horizontal spacing
        )

        self.player_id_entry.focus()                     # Places the typing cursor in Player ID


    def add_player(self):                                # Validates and adds a player
        player_id = self.player_id_entry.get().strip()   # Gets the entered player ID
        codename = self.codename_entry.get().strip()     # Gets the entered codename
        equipment_id = self.equipment_id_entry.get().strip()  # Gets the equipment ID
        team = self.selected_team.get()                  # Gets the selected team

        if not player_id or not codename or not equipment_id:  # Checks for empty fields
            messagebox.showerror(
                "Missing Information",
                "Enter the player ID, codename, and equipment ID"
            )
            return                                       # Stops the function

        if not player_id.isdigit():                      # Checks whether Player ID is an integer
            messagebox.showerror(
                "Invalid Player ID",
                "The player ID must be an integer"
            )
            return                                       # Stops the function

        if not equipment_id.isdigit():                   # Checks whether Equipment ID is an integer
            messagebox.showerror(
                "Invalid Equipment ID",
                "The equipment ID must be an integer"
            )
            return                                       # Stops the function

        player_id = int(player_id)                       # Converts Player ID into an integer
        equipment_id = int(equipment_id)                 # Converts Equipment ID into an integer

        all_players = self.red_players + self.green_players  # Combines both team lists

        for existing_player in all_players:              # Checks every existing player
            if existing_player["player_id"] == player_id:  # Checks for a duplicate Player ID
                messagebox.showerror(
                    "Duplicate Player",
                    "That player ID has already been entered"
                )
                return                                   # Stops the function

            if existing_player["equipment_id"] == equipment_id:  # Checks for duplicate equipment
                messagebox.showerror(
                    "Duplicate Equipment",
                    "That equipment ID is already being used"
                )
                return                                   # Stops the function

        if team == "red":                                # Checks whether red is selected
            selected_players = self.red_players          # Selects the red player list
            selected_listbox = self.red_listbox          # Selects the red display list
        else:                                            # Runs when green is selected
            selected_players = self.green_players        # Selects the green player list
            selected_listbox = self.green_listbox        # Selects the green display list

        if len(selected_players) >= 15:                  # Checks whether the team already has 15 players
            messagebox.showerror(
                "Team Full",
                "Each team can contain a maximum of 15 players"
            )
            return                                       # Stops the function

        player = {
            "player_id": player_id,                      # Stores the Player ID
            "codename": codename,                        # Stores the codename
            "equipment_id": equipment_id                 # Stores the Equipment ID
        }

        selected_players.append(player)                  # Adds the player to the selected team

        player_text = (
            f"{len(selected_players)}. "                 # Displays the player's team number
            f"{codename} | "                             # Displays the codename
            f"Player ID: {player_id} | "                 # Displays the Player ID
            f"Equipment: {equipment_id}"                 # Displays the Equipment ID
        )

        selected_listbox.insert(
            tk.END,                                      # Adds the player to the end of the list
            player_text                                  # Displays the player's information
        )

        self.clear_entry_fields()                        # Clears the fields for the next player


    def clear_entry_fields(self):                        # Clears the player entry text boxes
        self.player_id_entry.delete(0, tk.END)           # Clears Player ID
        self.codename_entry.delete(0, tk.END)            # Clears Codename
        self.equipment_id_entry.delete(0, tk.END)        # Clears Equipment ID
        self.player_id_entry.focus()                     # Returns the cursor to Player ID


    def clear_all_players(self, event=None):             # Removes all entered players
        if not self.red_players and not self.green_players:  # Checks whether both teams are empty
            return                                       # Stops when there is nothing to clear

        confirmed = messagebox.askyesno(
            "Clear All Players",
            "Are you sure you want to remove every player?"
        )

        if not confirmed:                                # Checks whether the operator selected No
            return                                       # Stops without clearing anything

        self.red_players.clear()                         # Removes stored red team players
        self.green_players.clear()                       # Removes stored green team players
        self.red_listbox.delete(0, tk.END)               # Clears the red team display
        self.green_listbox.delete(0, tk.END)             # Clears the green team display
        self.clear_entry_fields()                        # Clears the input fields


    def start_game(self, event=None):                    # Handles the Start Game control
        if not self.red_players and not self.green_players:  # Checks whether any players were entered
            messagebox.showwarning(
                "No Players",
                "Enter at least one player before starting the game"
            )
            return                                       # Stops the function

        messagebox.showinfo(
            "Start Game",
            "Player entry is complete and the gameplay screen will open here"
        )


if __name__ == "__main__":                               # Runs only when app.py is started directly
    root = tk.Tk()                                       # Creates the main Tkinter window
    app = LaserTagApp(root)                              # Creates the laser tag application
    root.mainloop()                                      # Keeps the application running