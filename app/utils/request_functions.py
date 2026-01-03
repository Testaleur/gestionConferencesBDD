def get_conferences_by_keywords(db_path, keywords):
  where_condition = " OR ".join(["LOWER(key_words) LIKE ?"] * len(keywords))
  params = [f"%{kw.lower()}%" for kw in keywords]

  query = f"""
  SELECT title, starting_date, key_words
  FROM conference
  WHERE {where_condition}
  ORDER BY starting_date DESC;
  """
  import sqlite3
  import pandas as pd
  conn = sqlite3.connect(db_path)
  df = pd.read_sql(query, conn, params=params)
  conn.close()
  return df
