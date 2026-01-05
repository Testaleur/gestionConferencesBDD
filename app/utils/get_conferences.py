import pandas as pd
import sqlite3
from utils.process_words import process_keywords
from utils.get_query import get_query_by_role_keywords, get_query_by_role_respo
  
def get_conferences_by_keywords(db_path, role, search_query, filters=None):
  search_words = process_keywords(search_query)
  params = [f"%{w}%" for w in search_words]

  query, extra_params = get_query_by_role_keywords(role, search_words, filters)
  params.extend(extra_params)

  conn = sqlite3.connect(db_path)
  df = pd.read_sql(query, conn, params=params)
  conn.close()
  return df

def get_conferences_by_responsable(db_path, id_responsable, role):
    
    query = get_query_by_role_respo(role)

    conn = sqlite3.connect(db_path)
    df = pd.read_sql(query, conn, params=[id_responsable])
    conn.close()
    return df
