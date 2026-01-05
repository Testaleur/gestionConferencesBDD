import sqlite3
import pandas as pd
from config import DB_PATH
from utils.get_query import get_query_upcoming
def get_upcoming(role):

  conn = sqlite3.connect(DB_PATH)

  query_upcoming = get_query_upcoming(role)
  
  upcoming = pd.read_sql(query_upcoming, conn)
  conn.close()

  return upcoming