import sqlite3

def edit_conference_from_base(DB_PATH, id_conference, request):
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()

  if request.method == "POST":
    title = request.form["title"]
    starting_date = request.form["starting_date"]
    ending_date = request.form["ending_date"]
    city = request.form["city"]
    country = request.form["country"]
    series = request.form["series"]
    introduction = request.form["introduction"]
    key_words = request.form["key_words"]
    editor = request.form["editor"]

    cursor.execute("""
      UPDATE conference
      SET title = ?, starting_date = ?, ending_date = ?, city = ?, country = ?,
        series = ?, introduction = ?, key_words = ?, editor = ?
      WHERE id_conference = ?
    """, (title, starting_date, ending_date, city, country,
      series, introduction, key_words, editor,
      id_conference))
    conn.commit()
    conn.close()
    return True
  else :
    return False
  
def get_conf_without_edit(DB_PATH, id_conference):
  conn = sqlite3.connect(DB_PATH)
  conn.row_factory = sqlite3.Row
  cursor = conn.cursor()
  cursor.execute("SELECT * FROM conference WHERE id_conference = ?", (id_conference,))
  conference = cursor.fetchone()
  conn.close()
  return conference

def edit_session_from_base(DB_PATH, id_session):
  pass

def edit_soumission_from_base(DB_PATH, id_soumission):
  pass