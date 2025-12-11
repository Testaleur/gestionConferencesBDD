import sqlite3
import pandas as pd

db_path = 'gestionConferences.db'
conn = sqlite3.connect(db_path)

# Lister les tables
tables = pd.read_sql_query("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name;", conn)
display(tables)

# Voir les colonnes de Utilisateur
schema_utilisateur = pd.read_sql_query("PRAGMA table_info(Utilisateur);", conn)
display(schema_utilisateur)

# (optionnel) Voir les colonnes des autres tables
schema_conference = pd.read_sql_query("PRAGMA table_info(Conference);", conn)
schema_session    = pd.read_sql_query("PRAGMA table_info(Session);", conn)
schema_personne   = pd.read_sql_query("PRAGMA table_info(Personne);", conn)
display(schema_conference, schema_session, schema_personne)

import sqlite3
import pandas as pd
from google.colab import files

# Télécharger le fichier depuis ton ordinateur
uploaded = files.upload()  # Choisis gestionConferences.db

# Connexion à la base
conn = sqlite3.connect("gestionConferences.db")

query = """
SELECT *
FROM CONFERENCE
WHERE strftime('%Y', "starting_date") = strftime('%Y', 'now');
"""

df = pd.read_sql(query, conn)
print(df.head())
conn.close()

import sqlite3
import pandas as pd

# Connexion à la base déjà uploadée
conn = sqlite3.connect("gestionConferences.db")

# Requête SQL : pays et liste des conférences
query = """
SELECT country, GROUP_CONCAT(title, ', ') AS Conferences, COUNT(title) AS Nb_Conferences
FROM CONFERENCE
GROUP BY country;
"""
# Charger le résultat dans un DataFrame Pandas
df = pd.read_sql(query, conn)

from IPython.display import display
display(df)

# Afficher le tableau dans Colab
df

# Fermer la connexion
conn.close()

import sqlite3
import pandas as pd
from IPython.display import display

# Connexion à la base
conn = sqlite3.connect("gestionConferences.db")

# Requête pour trouver les conférences liées aux bases de données spatiales
query = """
SELECT *
FROM CONFERENCE
WHERE "key_words" LIKE '%base%'
   OR "key_words" LIKE '%données%'
   OR "key_words" LIKE '%spatial%';
"""

# Charger le résultat dans un DataFrame
df = pd.read_sql(query, conn)

# Afficher le tableau
display(df)

# Fermer la connexion
conn.close()

import sqlite3
import pandas as pd

# 1) Connexion à la base
conn = sqlite3.connect('gestionConferences.db')

# 2) Requête SQL : mettre le SQL dans une chaîne triple-quoted
query = """
WITH RECURSIVE kw(kw, rest) AS (
  SELECT
    LOWER(TRIM(
      CASE
        WHEN instr(profile, ',') > 0 THEN substr(profile, 1, instr(profile, ',') - 1)
        ELSE profile
      END
    )) AS kw,
    CASE
      WHEN instr(profile, ',') > 0 THEN substr(profile, instr(profile, ',') + 1)
      ELSE ''
    END AS rest
  FROM utilisateur
  WHERE id_user = :userId

  UNION ALL

  SELECT
    LOWER(TRIM(
      CASE
        WHEN instr(rest, ',') > 0 THEN substr(rest, 1, instr(rest, ',') - 1)
        ELSE rest
      END
    )) AS kw,
    CASE
      WHEN instr(rest, ',') > 0 THEN substr(rest, instr(rest, ',') + 1)
      ELSE ''
    END AS rest
  FROM kw
  WHERE rest <> ''
)
SELECT DISTINCT c.id_conference, c.title, c.series, c.country
FROM conference c
LEFT JOIN session s ON s.id_conference = c.id_conference
WHERE EXISTS (
  SELECT 1
  FROM kw
  WHERE kw.kw <> '' AND (
        LOWER(COALESCE(c.key_words, '')) LIKE '%' || kw.kw || '%'
     OR LOWER(COALESCE(s.themes,    '')) LIKE '%' || kw.kw || '%'
  )
)
ORDER BY c.title;
"""

# 3) Exécution avec paramètre userId
df = pd.read_sql_query(query, conn, params={"userId": 12})
df.head()

import sqlite3
import pandas as pd

# 1) Connexion à la base
conn = sqlite3.connect('gestionConferences.db')

# 2) Écrire la requête dans une chaîne triple-quoted
query = """
SELECT id_conference, title, starting_date, ending_date, country, city
FROM conference
WHERE LOWER(series) = 'sdh'
ORDER BY starting_date;
"""

# 3) Exécuter la requête
df5 = pd.read_sql_query(query, conn)
df5.head()

pd.read_sql_query("""
SELECT id_conference, title, type, associated_conf
FROM conference
WHERE LOWER(type) = 'workshop'
LIMIT 10;
""", conn)

import sqlite3
import pandas as pd

conn = sqlite3.connect('gestionConferences.db')

query_all_workshops = """
SELECT w.id_conference AS workshop_id,
       w.title         AS workshop_title,
       w.starting_date AS workshop_start,
       w.ending_date   AS workshop_end,
       w.city          AS workshop_city,
       w.country       AS workshop_country,
       p.id_conference AS parent_id,
       p.title         AS parent_title,
       p.starting_date AS parent_start,
       p.ending_date   AS parent_end
FROM conference w
JOIN conference p ON p.id_conference = w.associated_conf
WHERE LOWER(w.type) = 'workshop'
ORDER BY p.title, w.starting_date;
"""

df_workshops_all = pd.read_sql_query(query_all_workshops, conn)
df_workshops_all

import sqlite3
import pandas as pd

# Connexion à la base
conn = sqlite3.connect('gestionConferences.db')

# Paramètre : ID de la conférence parente
parent_conf_id = 40

query = """
SELECT id_conference, title, starting_date, ending_date, city, country
FROM conference
WHERE LOWER(type) = 'workshop'
  AND associated_conf = :id_conf_parent
ORDER BY starting_date;
"""

df_workshops = pd.read_sql_query(query, conn, params={"id_conf_parent": parent_conf_id})
df_workshops

import sqlite3
import pandas as pd

conn = sqlite3.connect('gestionConferences.db')

query7 = """
SELECT id_conference, title, series, starting_date, country
FROM conference
WHERE LOWER(editor) = LOWER(:editor_name)
ORDER BY starting_date;
"""

df7 = pd.read_sql_query(query7, conn, params={"editor_name": "Almudena Constanza Blanca Barros"})
df7

import sqlite3
import pandas as pd

# Connexion
conn = sqlite3.connect('gestionConferences.db')

query8 = """
SELECT DISTINCT u.id_user, p.name, p.first_name, p.mail
FROM utilisateur u
JOIN personne    p ON p.id_personne   = u.id_personne
JOIN responsable r ON r.id_personne   = p.id_personne
LEFT JOIN direction  d ON d.id_responsable = r.id_responsable
LEFT JOIN evaluation e ON e.id_responsable = r.id_responsable
WHERE d.id_conference IS NOT NULL
   OR e.id_session    IS NOT NULL
ORDER BY p.name, p.first_name;
"""

df8 = pd.read_sql_query(query8, conn)
df8

import sqlite3
import pandas as pd

conn = sqlite3.connect('gestionConferences.db')

# Paramètres d'identification du professeur "X"
params = {
    "name": "Proctor",
    "first_name": "Jay",
    "email": "jay.proctor@university.edu"
}

query9 = """
-- Version UNION recommandée
SELECT DISTINCT
  c.id_conference,
  c.title,
  'responsable_conference' AS involvement_source
FROM personne p
JOIN responsable r ON r.id_personne = p.id_personne
JOIN direction  d ON d.id_responsable = r.id_responsable
JOIN conference c ON c.id_conference  = d.id_conference
WHERE (
        LOWER(p.name)       = LOWER(:name)
    AND LOWER(p.first_name) = LOWER(:first_name)
      )
   OR ( :email <> '' AND LOWER(p.mail) = LOWER(:email) )

UNION

SELECT DISTINCT
  c.id_conference,
  c.title,
  'membre_pc' AS involvement_source
FROM personne p
JOIN responsable r ON r.id_personne = p.id_personne
JOIN evaluation e ON e.id_responsable = r.id_responsable
JOIN session    s ON s.id_session     = e.id_session
JOIN conference c ON c.id_conference  = s.id_conference
WHERE (
        LOWER(p.name)       = LOWER(:name)
    AND LOWER(p.first_name) = LOWER(:first_name)
      )
   OR ( :email <> '' AND LOWER(p.mail) = LOWER(:email) )
ORDER BY title;
"""

df9 = pd.read_sql_query(query9, conn, params=params)
df9