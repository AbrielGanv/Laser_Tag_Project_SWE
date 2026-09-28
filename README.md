README

Team Members
GitHub Username | Real Name
----------------|----------
matthewworkman62-alt | Matthew Workman
BrittonAdair3        | Britton Adair
purge911             | Ibrahim Khan        
AbrielGanv           | Gabriel Vang      
Khanah2022           | Ahmed Khan

Requirements
- Debian-based Linux (Debian or Ubuntu)
- Python 3
- PostgreSQL
- Tkinter
- Pillow
- psycopg2

Installation
1. Open a terminal on the Debian or Ubuntu VM
2. Clone the GitHub repository: git clone https://github.com/AbrielGanv/Laser_Tag_Project_SWE
3. Move into the project folder: cd Laser_Tag_Project_SWE
4. Run the installation script: bash install.sh
5. Wait for all required packages to finish installing.

Running the Program
1. Make sure you are inside the project folder.
2. Run the application with: python3 app.py
3. The laser tag application should open.

Database
The program expects PostgreSQL to already contain:
Database: photon
Table: players

Networking
Default network address: 127.0.0.1
UDP transmit port: 7500
This can be configured while within the program. 

The network address can be changed inside the application.
