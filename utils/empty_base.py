
##########################################
# BE CAREFUL THIS WILL EMPTY THE WHOLE BASE
##########################################

from empty_table import empty_table

def empty_all_tables(db_path):
  """Empties all tables in the database."""
  tables = [
    "evaluation",
    "direction",
    "soumission",
    "session",
    "conference",
    "responsable",
    "utilisateur",
    "personne",
    "universite"
  ]
  
  for table in tables:
    empty_table(db_path, table)

  print("Base hase been emptied successfully.")

db_path = "gestionConferences.db"
empty_all_tables(db_path)