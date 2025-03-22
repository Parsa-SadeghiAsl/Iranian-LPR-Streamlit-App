import sqlite3
import pandas as pd
import os

class DatabaseManager:
  """
  This class manages interactions with the SQLite database.
  """

  def __init__(self, directory, filename):
    """
    Initializes the database connection.

    """
    db_path = os.path.join(directory, filename)
    
    if not os.path.exists(directory):
        # directory doesn't exist, create it
        os.makedirs(directory)

    self.conn = sqlite3.connect(db_path)
    self.conn.execute('PRAGMA encoding = "UTF-8"')
    self.cursor = self.conn.cursor()

  def create_recognized_plates_table(self):
    """
    Creates the 'recognized_plates' table if it doesn't already exist.
    """
    self.cursor.execute("""
    CREATE TABLE IF NOT EXISTS recognized_plates (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      plate_text TEXT COLLATE NOCASE,
      timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)
    self.conn.commit()

  def save_recognized_plate(self, plate_text):
    """
    Saves a recognized plate and its timestamp to the database.

    Args:
      plate_text (str): The text of the recognized plate.
    """
    self.cursor.execute("""
    INSERT INTO recognized_plates (plate_text)
    VALUES (?)
    """, (plate_text,))
    self.conn.commit()

  def get_all_recognized_plates(self):
    """
    Retrieves all recognized plates from the database as a pandas DataFrame.

    Returns:
      pd.DataFrame: DataFrame containing recognized plates and timestamps.
    """
    self.cursor.execute("SELECT * FROM recognized_plates")
    rows = self.cursor.fetchall()
    columns = [col[0] for col in self.cursor.description]
    return pd.DataFrame(rows, columns=columns)

  def close_connection(self):
    """
    Closes the connection to the database.
    """
    self.conn.close()
