import sqlite3
import pandas as pd
from utils.get_query import get_query_workshops_by_conf_id

def get_workshops_by_conf_id(DB_PATH, id_conference, role):
  conn = sqlite3.connect(DB_PATH) 

  query = get_query_workshops_by_conf_id(role, id_conference)

  df = pd.read_sql(query, conn)
  conn.close()
  
  return df