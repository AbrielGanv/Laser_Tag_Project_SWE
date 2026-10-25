# Photon Laser Tag

## Team Members

| GitHub Username | Real Name |
| --- | --- |
| matthewworkman62-alt | Matthew Workman |
| BrittonAdair3 | Britton Adair |
| purge911 | Ibrahim Khan |
| AbrielGanv | Gabriel Vang |
| Khanah2022 | Ahmed Khan |

## Installation

Use the Debian VM with PostgreSQL already set up.
The program expects a database named `photon` with a table named `players` containing `id` and `codename` columns.

1. Open a terminal.
2. Download the project:
   ```bash
   git clone https://github.com/AbrielGanv/Laser_Tag_Project_SWE
   ```
3. Open the project folder:
   ```bash
   cd Laser_Tag_Project_SWE
   ```
4. Install the Python dependencies:
   ```bash
   bash install.sh
   ```
5. Start the program:
   ```bash
   python3 app.py
   ```

Keep all project files together, including the `udp_files` folder and `logo.jpg`.

## Using the Program

1. Select the red or green team.
2. Enter a player ID and press Enter. Existing players will have their codename filled in.
3. Enter a codename if the player is new.
4. Enter the hardware ID in the Equipment ID box.
5. Click Add Player. Repeat for each player.

## Controls

- F5 / Start Game: Start the 30-second countdown, then show the team rosters on the play action screen.
- Esc: Cancel the countdown.
- F12 / Clear All: Clear the players and input fields on the entry screen. This is disabled during the countdown.

The network address can be changed on the player entry screen. The default is `127.0.0.1`, with transmit port `7500` and receive port `7501`.

Countdown images are optional. Without them, the timer displays numbers. Scoring and hit events are not implemented for Sprint 3.
