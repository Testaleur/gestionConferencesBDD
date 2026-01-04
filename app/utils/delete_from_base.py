import sqlite3

def delete_conference_from_base(DB_PATH, id_conference):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()

  # Delete related sessions, soumissions
  cursor.execute("DELETE FROM soumission WHERE id_conference = ?", (id_conference,))
  cursor.execute("DELETE FROM session WHERE id_conference = ?", (id_conference,))
  cursor.execute("DELETE FROM direction WHERE id_conference = ?", (id_conference,))

  # Delete the conference
  cursor.execute("DELETE FROM conference WHERE id_conference = ?", (id_conference,))

  conn.commit()
  conn.close()

def delete_session_from_base(DB_PATH, id_session):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute("DELETE FROM evaluation WHERE id_session = ?", (id_session,))
  cursor.execute("DELETE FROM session WHERE id_session = ?", (id_session,))
  conn.commit()
  conn.close()

def delete_soumission_from_base(DB_PATH, id_soumission):
  conn = sqlite3.connect(DB_PATH)
  cursor = conn.cursor()
  cursor.execute("DELETE FROM soumission WHERE id_soumission = ?", (id_soumission,))
  conn.commit()
  conn.close()