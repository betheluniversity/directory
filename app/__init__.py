import jinja2
import requests

from flask import Flask, render_template

app = Flask(__name__)


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/results")
def results():
    repeat = 10
    return render_template('results.html', repeat=repeat)


@app.route("/search")
def search():
    print "memes"
    print "We got here"
    repeat = 10
    # #return render_template('results.html', repeat=repeat)
