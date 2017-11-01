import jinja2
import requests

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/results")
def search():
    repeat = 10
    return render_template('results.html', repeat=repeat)
