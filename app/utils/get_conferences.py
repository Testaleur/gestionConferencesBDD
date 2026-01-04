import pandas as pd
import sqlite3
from utils.process_typed_request import process_typed_request
from utils.get_query import get_query_by_role_keywords
  
def get_conferences_by_keywords(db_path, role, search_query, filters=None):
  search_words = process_typed_request(search_query)
  params = [f"%{w}%" for w in search_words]

  query, extra_params = get_query_by_role_keywords(role, search_words, filters)
  params.extend(extra_params)

  conn = sqlite3.connect(db_path)
  df = pd.read_sql(query, conn, params=params)
  conn.close()
  return df