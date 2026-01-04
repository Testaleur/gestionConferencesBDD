import sqlite3
DB_PATH = "../gestionConferences.db"

# récupérer le nom associé à l'ID
def get_user_name(role, user_id):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  name = None

  if role == "Utilisateur":
    cursor.execute("SELECT p.name, p.first_name FROM utilisateur u JOIN personne p ON u.id_personne=p.id_personne WHERE u.id_user=?", (user_id,))
    row = cursor.fetchone()
    if row:
      name = f"{row[1]} {row[0]}"
  elif role == "Responsable":
    cursor.execute("SELECT p.name, p.first_name FROM responsable r JOIN personne p ON r.id_personne=p.id_personne WHERE r.id_responsable=?", (user_id,))
    row = cursor.fetchone()
    if row:
      name = f"{row[1]} {row[0]}"
  elif role == "Admin":
    name = "Administrateur"
  
  conn.close()
  return name