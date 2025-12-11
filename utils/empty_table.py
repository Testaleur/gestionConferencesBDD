import sqlite3

TABLE_NAME_TO_EMPTY = "utilisateur"

def empty_table(db_path, table_name):
  """
  Empty a table in SQLite by its name.
  
  Args:
      db_path (str): Path to your SQLite database file.
      table_name (str): Name of the table to be emptied.
  """
  conn = sqlite3.connect(db_path)
  cursor = conn.cursor()

  try:
    # Use f-string safely if table_name is trusted
    cursor.execute(f"DELETE FROM {table_name};")
    # Optional: reset AUTOINCREMENT counter
    cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table_name}';")
    conn.commit()
    print(f"Table '{table_name}' has been emptied successfully.")
  except sqlite3.Error as e:
    print(f"An error occurred: {e}")
  finally:
    conn.close()

empty_table("gestionConferences.db", TABLE_NAME_TO_EMPTY)