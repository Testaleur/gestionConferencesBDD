import sqlite3
from utils.process_words import process_profile
from utils.get_query import get_query_name_user, get_query_name_respo, get_query_user_profile
DB_PATH = "../gestionConferences.db"

# récupérer le nom associé à l'ID
def get_user_name(role, user_id):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  name = None

  if role == "Utilisateur":
    cursor.execute(get_query_name_user(), (user_id,))
    row = cursor.fetchone()
    if row:
      name = f"{row[1]} {row[0]}"
  elif role == "Responsable":
    cursor.execute(get_query_name_respo(), (user_id,))
    row = cursor.fetchone()
    if row:
      name = f"{row[1]} {row[0]}"
  elif role == "Admin":
    name = "Administrateur"
  
  conn.close()
  return name

def get_user_profile(user_id):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  profile = None

  cursor.execute(get_query_user_profile(), (user_id,))
  row = cursor.fetchone()

  if row:
    profile = row[0] # to do : process_profile(row[0])
  else :
    profile = ""
    
  conn.close()
  return profile