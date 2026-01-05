import pandas as pd
import sqlite3
from config import DB_PATH

def get_stats_pays():
  conn = sqlite3.connect(DB_PATH)
  df_pays = pd.read_sql("""
    SELECT country, COUNT(*) AS nb_conferences
    FROM conference
    GROUP BY country
    ORDER BY nb_conferences DESC
  """, conn)
  conn.close()
  return df_pays

def get_stats_serie():
  conn = sqlite3.connect(DB_PATH)
  df_serie = pd.read_sql("""
    SELECT series, COUNT(*) AS nb_conferences
    FROM conference
    GROUP BY series
    ORDER BY nb_conferences DESC
  """, conn)
  conn.close()
  return df_serie

def get_stats_workshops():
  conn = sqlite3.connect(DB_PATH)
  df_workshops = pd.read_sql("""
    SELECT c.title, COUNT(*) AS nb_workshops
    FROM conference c
    LEFT JOIN conference w ON w.associated_conf = c.id_conference
    WHERE w.type = 'Workshop'
    GROUP BY c.id_conference
    ORDER BY nb_workshops DESC
  """, conn)
  conn.close()
  return df_workshops

def get_stats_activity():
  conn = sqlite3.connect(DB_PATH)
  df_activity = pd.read_sql("""
    SELECT c.title,
      COUNT(DISTINCT s.id_session) AS nb_sessions,
      COUNT(DISTINCT sub.id_soumission) AS nb_soumissions,
      (COUNT(DISTINCT s.id_session) + COUNT(DISTINCT sub.id_soumission)) AS total_activity
    FROM conference c
    LEFT JOIN session s ON s.id_conference = c.id_conference
    LEFT JOIN soumission sub ON sub.id_conference = c.id_conference
    GROUP BY c.id_conference
    ORDER BY total_activity DESC
  """, conn)
  conn.close()
  return df_activity
