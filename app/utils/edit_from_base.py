import sqlite3

from utils.get_query import get_query_conf_by_id, get_query_update_conf

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

    query = get_query_update_conf()

    cursor.execute(query, (title, starting_date, ending_date, city, country,
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
  cursor.execute(get_query_conf_by_id(), (id_conference,))
  conference = cursor.fetchone()
  conn.close()
  return conference

def edit_session_from_base(DB_PATH, id_session):
  pass

def edit_soumission_from_base(DB_PATH, id_soumission):
  pass