def get_conference_view(role):
  if role == "Utilisateur":
    return "v_conference_utilisateur"
  elif role == "Responsable":
    return "v_conference_responsable"
  elif role == "Admin":
    return "v_conference_admin"
  else:
    raise ValueError("Rôle inconnu")