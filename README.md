# Gestion des conférences – Base de données & Application Web

**Dépôt GitHub**  
https://github.com/Testaleur/gestionConferencesBDD.git

---

## Réponses aux questions / requêtes SQL
Dossier : `/base_main_handlers`  
Utiliser le fichier : `requetes.ipynb`

---

## Partie Base de Données
Se rendre dans le dossier : `/base_main_handlers`

### Création de la base
- Fichier : `creation_base.ipynb`

### Création des vues
- Fichier : `creation_vues.ipynb`

### Remplissage de la base
- Fichier : `remplissage_base.ipynb`

### Exemples de requêtes
- Fichier : `requetes.ipynb`

---

## Partie Application Web
Se rendre dans le dossier : `/app`

### Prérequis
- Python **3.9+**
- `pip`

### Librairies utilisées
```bash
pip install flask pandas faker
```

### Lancer l’application
Depuis le dossier /app, run : 
```bash
python app.py
```
Puis ouvrir un navigateur à l’adresse : http://127.0.0.1:5000

### Utiliser l'app :
Mot de passe : bdd

### Fonctionnalités :
Affichage du profil
Affichage des 3 prochaines conférences
Recherche de conférences par mots-clés
Filtres (type, série, dates, conférences à venir / passées)
Détail d'une conférence
Editer, supprimer
Page de statistiques
Navigation entre les pages
...

### Projet réalisé avec :
Flask, SQLite et pandas.