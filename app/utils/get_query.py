from utils.get_view import get_conference_view

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

