from utils.get_view import get_conference_view

######################
####### DELETE #######
######################
def get_query_delete_by_conf(table):
  return f"""
    DELETE FROM {table} WHERE id_conference = ?
  """

def get_query_delete_by_session(table):
  return f"""
    DELETE FROM {table} WHERE id_session = ?
  """

def get_query_delete_by_soumission(table):
  return f"""
    DELETE FROM {table} WHERE id_soumission = ?
  """

######################
####### UPDATE #######
######################
def get_query_update_conf():
  return """
    UPDATE conference
    SET title = ?, starting_date = ?, ending_date = ?, city = ?, country = ?,
      series = ?, introduction = ?, key_words = ?, editor = ?
    WHERE id_conference = ?
  """

######################
####### SELECT #######
######################
def get_query_conf_by_id():
  return """
  SELECT * FROM conference WHERE id_conference = ?
  """

def get_query_stats_pays():
  return """
    SELECT country, COUNT(*) AS nb_conferences
    FROM conference
    GROUP BY country
    ORDER BY nb_conferences DESC
  """

def get_query_stats_serie():
  return"""
    SELECT series, COUNT(*) AS nb_conferences
    FROM conference
    GROUP BY series
    ORDER BY nb_conferences DESC
  """

def get_query_stats_workshops():
  return """
    SELECT c.title, COUNT(*) AS nb_workshops
    FROM conference c
    LEFT JOIN conference w ON w.associated_conf = c.id_conference
    WHERE w.type = 'Workshop'
    GROUP BY c.id_conference
    ORDER BY nb_workshops DESC
  """

def get_query_stats_activity():
  return """
    SELECT c.title,
      COUNT(DISTINCT s.id_session) AS nb_sessions,
      COUNT(DISTINCT sub.id_soumission) AS nb_soumissions,
      (COUNT(DISTINCT s.id_session) + COUNT(DISTINCT sub.id_soumission)) AS total_activity
    FROM conference c
    LEFT JOIN session s ON s.id_conference = c.id_conference
    LEFT JOIN soumission sub ON sub.id_conference = c.id_conference
    GROUP BY c.id_conference
    ORDER BY total_activity DESC
  """

def get_query_stats_confs():
  return """
  SELECT COUNT(*) AS total_conferences FROM conference;"""

def get_query_stats_workshops_vs_conf():
  return """
  SELECT 
    SUM(CASE WHEN type='Workshop' THEN 1 ELSE 0 END) AS nb_workshops,
    SUM(CASE WHEN type='Conference' THEN 1 ELSE 0 END) AS nb_conferences
  FROM conference;
  """

def get_query_stats_universite():
  return """
  SELECT u.name AS universite, COUNT(c.id_conference) AS nb_conferences
  FROM conference c
  LEFT JOIN universite u ON c.id_universite = u.id_universite
  GROUP BY u.name
  ORDER BY nb_conferences DESC;
  """

def get_query_name_user():
  return """
  SELECT p.name, p.first_name 
  FROM utilisateur u 
  JOIN personne p 
  ON u.id_personne=p.id_personne 
  WHERE u.id_user=?"""

def get_query_name_respo():
  return """
  SELECT p.name, p.first_name 
  FROM responsable r 
  JOIN personne p 
  ON r.id_personne=p.id_personne 
  WHERE r.id_responsable=?"""

def get_query_user_profile():
  return """
  SELECT profile 
  FROM utilisateur 
  WHERE id_user=?"""

def get_query_upcoming(role):
  view = get_conference_view(role)
  return f"""
    SELECT c.id_conference,
      c.title,
      c.starting_date,
      c.city,
      c.country,
      c.series,
      u.name AS universite_name,
      c2.title AS conf_associee
    FROM {view} c
    LEFT JOIN universite u ON c.id_universite = u.id_universite
    LEFT JOIN conference c2 ON c.associated_conf = c2.id_conference
    WHERE DATE(c.starting_date) >= DATE('now')
    ORDER BY DATE(c.starting_date) ASC
    LIMIT 3;
    """

def get_query_by_id(role, id_conference):
  view = get_conference_view(role)

  if role == "Utilisateur":
    query = f"""
      SELECT c.*, u.name AS universite_name, c2.title AS conf_associee
      FROM {view} c
      LEFT JOIN universite u ON c.id_universite = u.id_universite
      LEFT JOIN conference c2 ON c.associated_conf = c2.id_conference
      WHERE c.id_conference = {id_conference}
    """
  elif role == "Responsable":
    query = f"""
      SELECT c.*, u.name AS universite_name, c2.title AS conf_associee
      FROM {view} c
      LEFT JOIN universite u ON c.id_universite = u.id_universite
      LEFT JOIN conference c2 ON c.associated_conf = c2.id_conference
      WHERE c.id_conference = {id_conference}
    """
  else:  # Admin
    query = f"""
      SELECT c.*, u.name AS universite_name, c2.title AS conf_associee
      FROM {view} c
      LEFT JOIN universite u ON c.id_universite = u.id_universite
      LEFT JOIN conference c2 ON c.associated_conf = c2.id_conference
      WHERE c.id_conference = {id_conference}
    """
  return query

def get_query_by_role_keywords(role, words, filters=None):
  view = get_conference_view(role)
  conditions = []
  params_extra = []

  # Mots-clés
  if words:
    where_clause = " OR ".join([f"LOWER(c.key_words) LIKE ?" for w in words])
    conditions.append(f"({where_clause})")

  # Filtres dynamiques
  if filters:
    # Type
    if "type" in filters and filters["type"]:
      placeholders = ",".join(["?"] * len(filters["type"]))
      conditions.append(f"c.type IN ({placeholders})")
      params_extra.extend(filters["type"])

    # Série
    if "serie" in filters and filters["serie"]:
      conditions.append("c.series = ?")
      params_extra.append(filters["serie"])

    # Année
    if "year" in filters and filters["year"]:
      conditions.append("strftime('%Y', c.starting_date) = ?")
      params_extra.append(filters["year"])

    # Période
    if "date_start" in filters and filters["date_start"]:
      conditions.append("c.starting_date >= ?")
      params_extra.append(filters["date_start"])
    if "date_end" in filters and filters["date_end"]:
      conditions.append("c.ending_date <= ?")
      params_extra.append(filters["date_end"])

    # À venir / passées
    if "time_status" in filters:
      if filters["time_status"] == "future":
        conditions.append("c.starting_date >= date('now')")
      elif filters["time_status"] == "past":
        conditions.append("c.starting_date < date('now')")

    # Jointures communes
    query_base = f"""
    SELECT c.*, u.name AS universite_name, c2.title AS conf_associee
    FROM {view} c
    LEFT JOIN universite u ON c.id_universite = u.id_universite
    LEFT JOIN conference c2 ON c.associated_conf = c2.id_conference
    """

  # WHERE dynamique
  if conditions:
    query_base += " WHERE " + " AND ".join(conditions)

  query_base += " ORDER BY c.starting_date DESC"

  return query_base, params_extra

def get_query_by_role_respo(role):
  view = get_conference_view(role)

  query = f"""
      SELECT c.*, u.name AS universite_name, c2.title AS conf_associee
      FROM {view} c
      LEFT JOIN universite u ON c.id_universite = u.id_universite
      LEFT JOIN conference c2 ON c.associated_conf = c2.id_conference
      JOIN direction d ON c.id_conference = d.id_conference
      WHERE d.id_responsable = ?
      ORDER BY c.starting_date DESC;
  """
  return query

def get_query_session_by_conf_id(role, id_conference):
  return f"""
		SELECT s.*
		FROM session s
		WHERE s.id_conference = {id_conference}
	"""

def get_query_responsables_by_conf_id(id_conference):
  return f"""
		SELECT r.id_responsable, r.pro_adress, r.type, p.name AS person_name, p.first_name
		FROM direction d
		JOIN responsable r ON d.id_responsable = r.id_responsable
		JOIN personne p ON r.id_personne = p.id_personne
		WHERE d.id_conference = {id_conference}
	"""

def get_query_soumissions_by_conf_id(role, id_conference):
  return f"""
		SELECT *
		FROM soumission
		WHERE id_conference = {id_conference}
	"""

def get_query_workshops_by_conf_id(role, id_conference):
  return f"""
		SELECT c.id_conference, c.title
		FROM conference c
		WHERE c.type = 'Workshop' AND c.associated_conf = {id_conference}
	"""