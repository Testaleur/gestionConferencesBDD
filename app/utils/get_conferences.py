import pandas as pd
import sqlite3
from utils.process_typed_request import process_typed_request

def get_conference_view(role):
  if role == "Utilisateur":
    return "v_conference_utilisateur"
  elif role == "Responsable":
    return "v_conference_responsable"
  elif role == "Admin":
    return "v_conference_admin"
  else:
    raise ValueError("Rôle inconnu")
  
def get_query_by_role(role, words):
  view = get_conference_view(role)
  where_clause = " OR ".join([f"LOWER(c.key_words) LIKE ?" for w in words])

  if role == "Utilisateur":
    # On joint quand même université et conf associée pour avoir les noms lisibles
    query = f"""
      SELECT c.*, u.name AS universite_name, c2.title AS conf_associee
      FROM {view} c
      LEFT JOIN universite u ON c.id_universite = u.id_universite
      LEFT JOIN conference c2 ON c.associated_conf = c2.id_conference
      WHERE {where_clause}
      ORDER BY c.starting_date DESC;
    """
  elif role == "Responsable":
    query = f"""
      SELECT c.*, u.name AS universite_name, c2.title AS conf_associee
      FROM {view} c
      LEFT JOIN universite u ON c.id_universite = u.id_universite
      LEFT JOIN conference c2 ON c.associated_conf = c2.id_conference
      WHERE {where_clause}
      ORDER BY c.starting_date DESC;
    """
  else:  # Admin
    query = f"""
      SELECT c.*, u.name AS universite_name, c2.title AS conf_associee
      FROM {view} c
      LEFT JOIN universite u ON c.id_universite = u.id_universite
      LEFT JOIN conference c2 ON c.associated_conf = c2.id_conference
      WHERE {where_clause}
      ORDER BY c.starting_date DESC;
    """
  return query

def get_conferences_by_keywords(db_path, role, keywords):
  words = process_typed_request(keywords)
  params = [f"%{w}%" for w in words]

  query = get_query_by_role(role, words)

  conn = sqlite3.connect(db_path)
  df = pd.read_sql(query, conn, params=params)
  conn.close()
  return df