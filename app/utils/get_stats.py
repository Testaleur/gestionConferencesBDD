import pandas as pd
import sqlite3
from config import DB_PATH
from utils.get_query import get_query_stats_pays, get_query_stats_activity, get_query_stats_confs, get_query_stats_serie, get_query_stats_universite, get_query_stats_workshops, get_query_stats_workshops_vs_conf

def get_stats_pays():
  conn = sqlite3.connect(DB_PATH)
  df_pays = pd.read_sql(get_query_stats_pays(), conn)
  conn.close()
  return df_pays

def get_stats_serie():
  conn = sqlite3.connect(DB_PATH)
  df_serie = pd.read_sql(get_query_stats_serie(), conn)
  conn.close()
  return df_serie

def get_stats_workshops():
  conn = sqlite3.connect(DB_PATH)
  df_workshops = pd.read_sql(get_query_stats_workshops(), conn)
  conn.close()
  return df_workshops

def get_stats_activity():
  conn = sqlite3.connect(DB_PATH)
  df_activity = pd.read_sql(get_query_stats_activity(), conn)
  conn.close()
  return df_activity

def get_stats_total_conferences():
  conn = sqlite3.connect(DB_PATH)
  query = get_query_stats_confs()
  df = pd.read_sql(query, conn)
  conn.close()
  return df

def get_stats_workshops_vs_conferences():
  conn = sqlite3.connect(DB_PATH)
  query = get_query_stats_workshops_vs_conf()
  df = pd.read_sql(query, conn)
  conn.close()
  return df

def get_stats_by_universite():
  conn = sqlite3.connect(DB_PATH)
  query = get_query_stats_universite()
  df = pd.read_sql(query, conn)
  conn.close()
  return df
