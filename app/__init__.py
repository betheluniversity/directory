import jinja2

from flask import Flask, render_template, request
from app import person, query
app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/results")
def results():
    repeat = 10
    return render_template('results.html', repeat=repeat)


@app.route("/search", methods=["POST"])
def search():
    data = request.form
    # The Query
    search_for = query.Query(data["firstName"], data['lastName'])

    if "Students" in data:
        search_for.__set__("student", data['Students'])
    if "Pictures" in data:
        search_for.__set__("picture", data['Students'])
    if "Groups" in data:
        search_for.__set__("groups", data['Students'])
    if "Home" in data:
        search_for.__set__("home", data['Students'])
    if "Staff" in data:
        search_for.__set__("teacher", data['Students'])

    repeat = 5
    return render_template('results.html', repeat=repeat, query=search_for)
