import pandas as pd
import sqlite3

def get_conference_view(role):
  if role == "Utilisateur":
    return "v_conference_utilisateur"
  elif role == "Responsable":
    return "v_conference_responsable"
  elif role == "Admin":
    return "v_conference_admin"
  else:
    raise ValueError("Rôle inconnu")

def get_conferences_by_keywords(db_path, role, keywords):
  view = get_conference_view(role)

  where_condition = " OR ".join(["LOWER(key_words) LIKE ?"] * len(keywords))
  params = [f"%{kw.lower()}%" for kw in keywords]

  query = f"""
    SELECT *
    FROM {view}
    WHERE {where_condition}
    ORDER BY starting_date DESC;
  """

  conn = sqlite3.connect(db_path)
  df = pd.read_sql(query, conn, params=params)
  conn.close()
  return df