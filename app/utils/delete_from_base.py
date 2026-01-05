import sqlite3
from utils.get_query import get_query_delete_by_conf, get_query_delete_by_session, get_query_delete_by_soumission

def delete_conference_from_base(DB_PATH, id_conference):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()

  # Delete related sessions, soumissions
  cursor.execute(get_query_delete_by_conf("soumission"), (id_conference,))
  cursor.execute(get_query_delete_by_conf("session"), (id_conference,))
  cursor.execute(get_query_delete_by_conf("direction"), (id_conference,))

  # Delete the conference
  cursor.execute(get_query_delete_by_conf("conference"), (id_conference,))

  conn.commit()
  conn.close()

def delete_session_from_base(DB_PATH, id_session):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute(get_query_delete_by_session("evaluation"), (id_session,))
  cursor.execute(get_query_delete_by_session("session"), (id_session,))
  conn.commit()
  conn.close()

def delete_soumission_from_base(DB_PATH, id_soumission):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute(get_query_delete_by_soumission("soumission"), (id_soumission,))
  conn.commit()
  conn.close()