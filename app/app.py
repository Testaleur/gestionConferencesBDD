from flask import Flask, render_template, request, redirect, url_for, session
from utils.get_conferences import get_conferences_by_keywords
from utils.get_user_infos import get_user_name

app = Flask(__name__)
DB_PATH = "../gestionConferences.db"
PASSWORD = "bdd"  # mot de passe constant commun
app.secret_key = "secretkey"  # nécessaire pour la session

# login page
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        role = request.form.get("role")
        user_id = request.form.get("user_id")  # peut être vide si Admin
        password = request.form.get("password")

        # Vérification mot de passe
        if password != PASSWORD:
            error = "Mot de passe incorrect"
        else:
            # Vérification de l'existence de l'ID
            if role == "Admin":
                session['role'] = role
                session['user_id'] = 0
                session['name'] = "Administrateur"
                return redirect(url_for("index"))
            elif user_id and user_id.isdigit():
                name = get_user_name(role, int(user_id))
                if name:
                    session['role'] = role
                    session['user_id'] = int(user_id)
                    session['name'] = name
                    return redirect(url_for("index"))
                else:
                    error = f"ID {user_id} introuvable pour le rôle {role}"
            else:
                error = "Veuillez entrer un ID valide"

    return render_template("login.html", error=error)

# Page principale
@app.route("/index", methods=["GET", "POST"])
def index():
    if 'role' not in session:
        return redirect(url_for("login"))

    results = None
    if request.method == "POST":
        search_query = request.form.get("search")
        if search_query:
            keywords = search_query.split()
            results = get_conferences_by_keywords(DB_PATH, session['role'], keywords)
    return render_template("index.html", results=results, role=session['role'], name=session['name'], user_id=session['user_id'])

# déconnexion
@app.route("/logout")
def logout():
  session.clear()
  return redirect(url_for("login"))

if __name__ == "__main__":
  app.run(debug=True)