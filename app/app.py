from flask import Flask, render_template, request, redirect, url_for, session, flash
from utils.get_conferences import get_conferences_by_keywords
from utils.get_user_infos import get_user_name
from utils.get_conf_by_id import get_conf_by_id
from utils.get_sessions_by_conf_id import get_sessions_by_conf_id
from utils.get_responsables_by_conf_id import get_responsables_by_conf_id
from utils.get_workshops_by_conf_id import get_workshops_by_conf_id
from utils.get_soumissions_by_conf_id import get_soumissions_by_conf_id
from utils.delete_from_base import delete_conference_from_base, delete_session_from_base, delete_soumission_from_base
from utils.edit_from_base import edit_conference_from_base, get_conf_without_edit
from config import PASSWORD, DB_PATH

app = Flask(__name__)
app.secret_key = "secretkey"

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
  sessions = get_sessions_by_conf_id(DB_PATH, id_conference, role)
  workshops = get_workshops_by_conf_id(DB_PATH, id_conference, role)
  responsables = get_responsables_by_conf_id(DB_PATH, id_conference, role)
  soumissions = get_soumissions_by_conf_id(DB_PATH, id_conference, role)

  return render_template(
    "conf_details.html",
    conf=conf,
    role=role,
    name=session['name'], 
    user_id=session['user_id'],
		sessions=sessions,
		workshops=workshops,
		responsables=responsables,
		soumissions=soumissions
  )

# back to results
@app.route("/back", methods=["GET", "POST"])
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

# delete conference
@app.route("/delete_conference/<int:id_conference>", methods=["POST"])
def delete_conference(id_conference):
  # Only Admin or Responsable can delete
  if session['role'] not in ['Admin', 'Responsable']:
    flash("Vous n'avez pas le droit de supprimer de conférence.")
    return redirect(url_for("index"))
  
  delete_conference_from_base(DB_PATH, id_conference)
  return redirect(url_for("index"))

# delete session
@app.route("/delete_session/<int:id_session>", methods=["POST"])
def delete_session(id_session):
  if session['role'] not in ['Admin', 'Responsable']:
    flash("Vous n'avez pas le droit de supprimer cette session.")
    return redirect(url_for("index"))
  
  delete_session_from_base(DB_PATH, id_session)
  return redirect(request.referrer or url_for("index"))

# delete soumission
@app.route("/delete_soumission/<int:id_soumission>", methods=["POST"])
def delete_soumission(id_soumission):
  if session['role'] not in ['Admin', 'Responsable']:
    flash("Vous n'avez pas le droit de supprimer cette soumission.")
    return redirect(url_for("index"))
  
  delete_soumission_from_base(DB_PATH, id_soumission)
  return redirect(request.referrer or url_for("index"))

@app.route("/edit_conference/<int:id_conference>", methods=["GET", "POST"])
def edit_conference(id_conference):
  if session['role'] not in ['Admin', 'Responsable']:
    flash("Vous n'avez pas le droit d'éditer cette conférence.")
    return redirect(url_for("index"))

  edit = edit_conference_from_base(DB_PATH, id_conference, request)
  if edit :
    flash("Conférence mise à jour avec succès.")
    return redirect(url_for("conference_detail", id_conference=id_conference))
  else :
    # sinon GET : afficher le formulaire avec les valeurs existantes
    conf = get_conf_without_edit(DB_PATH, id_conference)
    return render_template(
      "edit_conference.html", 
      conference=conf, 
      role=session['role'],
      name=session['name'], 
      user_id=session['user_id'],
    )

if __name__ == "__main__":
  app.run(debug=True)