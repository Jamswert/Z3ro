import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "guild-settings.db"

def get_connection():
    """A Helper function to get the connection to the database."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def add_guild(guild_id: int):
    """A function to add a guild to the database if it isn't already found.
    Parameters:
        - guild_id : int
            the ID of the guild you would like to add.
    """
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT OR IGNORE INTO guild_settings (guild_id)
        VALUES (?)
    """, (guild_id,))
    conn.commit()
    conn.close()

def toggle_guild_setting(guild_id: int, setting: str) -> bool:
    """A function that toggles the setting for a guild in the database.
    Parameters:
        - guild_id : int = the ID of the guild you would like to update the setting for.
        - setting : str = the name of the setting you want to toggle.
        
    Returns:
        - new_value : bool = This is the value after toggling the setting."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"SELECT {setting} FROM guild_settings WHERE guild_id = ?", (guild_id,))
    current = cur.fetchone()
    if not current:
        conn.close()
        raise ValueError(f"No guild found with id {guild_id}")

    current_value = current[0] or 0
    new_value = 0 if current_value else 1

    cur.execute(f"UPDATE guild_settings SET {setting} = ? WHERE guild_id = ?", (new_value, guild_id))
    conn.commit()
    conn.close()

    return bool(new_value)

def get_guild(guild_id: int):
    """A function that fetches the entire guild's row.
    Parameters:
        - guild_id : int = The ID of the guild you want to pull the row for.
        
    Returns:
        - row : dict = The guild's entire row. Can be accessed like:
            - row['logging_enabled']
            - row['welcome_enabled']"""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM guild_settings WHERE guild_id = ?", (guild_id,))
    row = cur.fetchone()
    conn.close()
    return row  # Access like a dict: row['logging_enabled'], row['welcome_enabled']