from flask import Flask, render_template, request
from utils.request_functions import get_conferences_by_keywords

app = Flask(__name__)
DB_PATH = "../gestionConferences.db"

@app.route("/", methods=["GET", "POST"])
def index():
  results = None
  if request.method == "POST":
    search_query = request.form.get("search")
    if search_query:
      keywords = search_query.split()
      results = get_conferences_by_keywords(DB_PATH, keywords)
  return render_template("index.html", results=results)

if __name__ == "__main__":
  app.run(debug=True)
