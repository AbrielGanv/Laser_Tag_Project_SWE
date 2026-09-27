import os                                                # Reads database settings from the environment
import sys                                               # Reads command-line arguments
import psycopg2                                          # Connects to the PostgreSQL database


MAX_CODENAME_LENGTH = 30                                 # Matches the codename column size in the players table


class PlayerDatabaseError(Exception):                    # Reports database connection and query problems
    pass                                                 # Works like a normal exception


def _default_connection_params():                        # Creates the database connection settings
    params = {
        "dbname": os.environ.get("PHOTON_DB_NAME", "photon") # Uses the photon database by default
    }

    optional = {
        "user": "PHOTON_DB_USER",                        # Stores the setting name for the user
        "password": "PHOTON_DB_PASSWORD",                # Stores the setting name for the password
        "host": "PHOTON_DB_HOST",                        # Stores the setting name for the address
        "port": "PHOTON_DB_PORT"                         # Stores the setting name for the port
    }

    for key, env_var in optional.items():                # Loops through each optional setting
        value = os.environ.get(env_var)                  # Gets the setting if one was provided
        if value:                                        # Checks whether the setting was provided
            params[key] = value                          # Adds the setting to the connection

    return params                                        # Returns the finished settings


def _validate_player_id(player_id):                      # Checks and converts a Player ID
    try:
        value = int(str(player_id).strip())              # Converts the Player ID into an integer
    except (TypeError, ValueError):                      # Runs when the Player ID is not a number
        raise ValueError(f"Player ID must be a whole number, got {player_id!r}")

    if value < 0:                                        # Checks whether the Player ID is negative
        raise ValueError("Player ID can't be negative")

    return value                                         # Returns the valid Player ID


def _validate_codename(codename):                        # Checks and cleans up a codename
    if codename is None:                                 # Checks whether a codename was given
        raise ValueError("Codename can't be empty")

    value = str(codename).strip()                        # Removes extra spaces from the codename

    if not value:                                        # Checks whether the codename is empty
        raise ValueError("Codename can't be empty")

    if len(value) > MAX_CODENAME_LENGTH:                 # Checks whether the codename is too long
        raise ValueError(
            f"Codename can be at most {MAX_CODENAME_LENGTH} characters "
            f"(got {len(value)})"
        )

    return value                                         # Returns the valid codename


class PlayerDatabase:                                    # Controls the connection to the photon database

    def __init__(self, **connection_params):             # Runs when the database object is created
        self._params = _default_connection_params()      # Gets the default connection settings
        self._params.update(
            {k: v for k, v in connection_params.items() if v} # Replaces defaults with any settings passed in
        )
        self._conn = None                                # Stores the connection once it opens


    def connect(self):                                   # Opens the database connection when needed
        if self._conn is None or self._conn.closed:      # Checks whether the connection needs opening
            try:
                self._conn = psycopg2.connect(**self._params) # Opens the connection
            except psycopg2.Error as error:              # Runs when the database can't be reached
                raise PlayerDatabaseError(
                    f"Could not connect to database "
                    f"'{self._params.get('dbname')}': {error}".strip()
                ) from error

        return self._conn                                # Returns the open connection


    def close(self):                                     # Closes the database connection
        if self._conn is not None and not self._conn.closed: # Checks whether a connection is open
            self._conn.close()                           # Closes the connection

        self._conn = None                                # Forgets the old connection


    def __enter__(self):                                 # Runs at the start of a with block
        self.connect()                                   # Opens the connection
        return self                                      # Returns the database object


    def __exit__(self, exc_type, exc, tb):               # Runs at the end of a with block
        self.close()                                     # Closes the connection


    def _run(self, query, args=(), fetch="none"):        # Runs one query safely
        conn = self.connect()                            # Gets an open connection

        try:
            with conn:                                   # Saves changes on success and undoes them on errors
                with conn.cursor() as cur:               # Creates a cursor for the query
                    cur.execute(query, args)             # Runs the query with its values

                    if fetch == "one":                   # Checks whether one row is wanted
                        return cur.fetchone()            # Returns one row

                    if fetch == "all":                   # Checks whether every row is wanted
                        return cur.fetchall()            # Returns every row

                    return cur.rowcount                  # Returns how many rows were changed
        except psycopg2.InterfaceError as error:         # Runs when the connection was lost
            self._conn = None                            # Forgets the lost connection so the next call reconnects
            raise PlayerDatabaseError(f"Lost connection to database: {error}") from error
        except psycopg2.Error as error:                  # Runs when the query fails
            raise PlayerDatabaseError(f"Database error: {error}".strip()) from error


    def get_codename(self, player_id):                   # Finds the codename for a Player ID
        pid = _validate_player_id(player_id)             # Checks the Player ID

        row = self._run(
            "SELECT codename FROM players WHERE id = %s LIMIT 1;", # Searches for the Player ID
            (pid,),                                      # Passes the Player ID safely
            fetch="one"                                  # Gets at most one row
        )

        return row[0] if row else None                   # Returns the codename or None when not found


    def player_exists(self, player_id):                  # Checks whether a Player ID is saved
        return self.get_codename(player_id) is not None  # Returns True when the player was found


    def add_player(self, player_id, codename):           # Saves a new player
        pid = _validate_player_id(player_id)             # Checks the Player ID
        name = _validate_codename(codename)              # Checks the codename

        if self.player_exists(pid):                      # Checks for a duplicate Player ID
            return False                                 # Stops without adding the player

        self._run(
            "INSERT INTO players (id, codename) VALUES (%s, %s);", # Adds the player to the table
            (pid, name)                                  # Passes the Player ID and codename safely
        )

        return True                                      # Reports that the player was added


    def delete_player(self, player_id):                  # Removes a player
        pid = _validate_player_id(player_id)             # Checks the Player ID

        deleted = self._run(
            "DELETE FROM players WHERE id = %s;",        # Removes the player from the table
            (pid,)                                       # Passes the Player ID safely
        )

        return deleted > 0                               # Reports whether a player was removed


    def get_all_players(self):                           # Gets every saved player
        return self._run(
            "SELECT id, codename FROM players ORDER BY id;", # Gets every player sorted by ID
            fetch="all"                                  # Gets every row
        )


_USAGE = """usage:
  python3 database.py list
  python3 database.py get <id>
  python3 database.py add <id> <codename>
  python3 database.py delete <id>"""


def _main(argv):                                         # Tests the database from the command line
    if not argv or argv[0] in ("-h", "--help"):          # Checks whether help was requested
        print(_USAGE)                                    # Shows the usage instructions
        return 0                                         # Stops the function

    command, args = argv[0], argv[1:]                    # Separates the command from its values

    try:
        with PlayerDatabase() as db:                     # Opens the database and closes it when done
            if command == "list" and not args:           # Runs the list command
                rows = db.get_all_players()              # Gets every player

                if not rows:                             # Checks whether the table is empty
                    print("(no players)")                # Reports an empty table

                for pid, name in rows:                   # Loops through every player
                    print(f"{pid:>6}  {name}")           # Displays the Player ID and codename

            elif command == "get" and len(args) == 1:    # Runs the get command
                name = db.get_codename(args[0])          # Looks up the codename
                print(name if name is not None else f"No player with id {args[0]}")

            elif command == "add" and len(args) >= 2:    # Runs the add command
                codename = " ".join(args[1:])            # Allows codenames with spaces

                if db.add_player(args[0], codename):     # Checks whether the player was added
                    print(f"Added player {args[0]}: {codename}")
                else:                                    # Runs when the Player ID already exists
                    print(f"Player {args[0]} already exists: {db.get_codename(args[0])}")
                    return 1                             # Reports a failure

            elif command == "delete" and len(args) == 1: # Runs the delete command
                if db.delete_player(args[0]):            # Checks whether the player was removed
                    print(f"Deleted player {args[0]}")
                else:                                    # Runs when the Player ID was not found
                    print(f"No player with id {args[0]}")
                    return 1                             # Reports a failure

            else:                                        # Runs when the command is not recognized
                print(_USAGE)                            # Shows the usage instructions
                return 2                                 # Reports incorrect usage
    except (ValueError, PlayerDatabaseError) as error:   # Runs when the input or database has a problem
        print(f"Error: {error}", file=sys.stderr)        # Displays the error
        return 1                                         # Reports a failure

    return 0                                             # Reports success


if __name__ == "__main__":                               # Runs only when database.py is started directly
    sys.exit(_main(sys.argv[1:]))                        # Runs the command and returns its result