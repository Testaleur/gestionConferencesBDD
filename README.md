-- git:
https://github.com/Testaleur/gestionConferencesBDD.git

-- réponses aux questions/requêtes:
utiliser le fichier /base_main_handlers/requetes.ipynb

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
PARTIE BDD - se rendre dans le dossier /base_main_handlers
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
-- créer la base:
utiliser le fichier creation_base.ipynb

-- créer les vues:
utiliser le fichier creation_vues.ipynb

-- remplir la base:
utiliser le fichier remplissage_base.ipynb

-- voir quelques requêtes :
utiliser le fichier requetes.ipynb

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
PARTIE APPLICATION - se rendre dans le dossier /app
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

-- Prérequis:
Python 3.9+
pip

-- Librairies utilisées :
pip install flask pandas faker

-- Lancer l’application
Depuis le dossier /app, run : python app.py
Puis ouvrir un navigateur à l’adresse : http://127.0.0.1:5000

-- Utiliser l'app :
Mot de passe : bdd

-- Fonctionnalités :
Affichage du profil
Affichage des 3 prochaines conférences
Recherche de conférences par mots-clés
Filtres (type, série, dates, conférences à venir / passées)
Détail d'une conférence
Editer, supprimer
Page de statistiques
Navigation entre les pages
...

-- Projet réalisé avec :
Flask, SQLite et pandas.