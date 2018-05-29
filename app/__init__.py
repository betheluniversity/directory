import datetime

from flask import Flask

from app import person, query

app = Flask(__name__)
app.config.from_object('config')
from app.db import db_functions as db

# Shows the year for the template
app.jinja_env.globals.update(now=datetime.datetime.now())

from app.views.home import HomeView
HomeView.register(app, route_base='/')

from app.views.results import ResultsView
ResultsView.register(app, route_base='/search/')
