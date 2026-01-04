from flask import Flask, render_template, request, redirect, url_for, session
from utils.get_conferences import get_conferences_by_keywords
from utils.get_user_infos import get_user_name
from utils.get_conf_by_id import get_conf_by_id

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
                session['last_role'] = role
                session['user_id'] = 0
                session['name'] = "Administrateur"
                session["last_search"] = ""
                session["last_filters"] = {}
                return redirect(url_for("index"))
            elif user_id and user_id.isdigit():
                name = get_user_name(role, int(user_id))
                if name:
                    session['role'] = role
                    session['last_role'] = role
                    session['user_id'] = int(user_id)
                    session['name'] = name
                    session["last_search"] = ""
                    session["last_filters"] = {}
                    return redirect(url_for("index"))
                else:
                    error = f"ID {user_id} introuvable pour le rôle {role}"
            else:
                error = "Veuillez entrer un ID valide"

    return render_template("login.html", error=error)
# déconnexion
@app.route("/logout")
def logout():
  session.clear()
  return redirect(url_for("login"))

# Page principale
@app.route("/index", methods=["GET", "POST"])
def index():
  if 'role' not in session:
    return redirect(url_for("login"))

  results = None
  if request.method == "POST":
    search_query = request.form.get("keywords", "")
    filters = {
      "type": request.form.getlist("type"),
      "serie": request.form.get("serie"),
      "year": request.form.get("year"),
      "date_start": request.form.get("date_start"),
      "date_end": request.form.get("date_end"),
      "time_status": request.form.get("time_status")
    }

    if search_query or filters:
      session["last_search"] = search_query
      session["last_filters"] = filters
      results = get_conferences_by_keywords(DB_PATH, session['role'], search_query, filters)

  return render_template(
     "index.html", 
     results=results, 
     role=session['role'], 
     name=session['name'], 
     user_id=session['user_id'],
     search_query=session['last_search'],
     filters=session["last_filters"]
    )

# open conference informations
@app.route("/conference/<int:id_conference>")
def conference_detail(id_conference):
	if "role" not in session:
		return redirect(url_for("login"))

	role = session["role"]
	conf = get_conf_by_id(DB_PATH, id_conference, role)

	return render_template(
		"conf_details.html",
		conf=conf,
		role=role,
    name=session['name'], 
    user_id=session['user_id']
	)

# back to results
@app.route("/back")
def back_to_results():
	if ("last_search" not in session and "last_filters" not in session) or "last_role" not in session:
		return redirect(url_for("index"))

	search_query = session["last_search"]
	filters = session["last_filters"]
	role = session["last_role"]

	results = get_conferences_by_keywords(DB_PATH, role, search_query, filters)

	return render_template(
		"index.html",
		results=results,
		role=role,
    name=session['name'], 
    user_id=session['user_id'],
    search_query=session['last_search'],
    filters=session["last_filters"]
	)

if __name__ == "__main__":
  app.run(debug=True)