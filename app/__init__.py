from flask import Flask
from flask.ext.cache import Cache

app = Flask(__name__)
app.config.from_object('config')
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
## TODO: Production cache

from app.db import db_functions as db

from app.views.home import HomeView
HomeView.register(app, route_base='/')

from app.views.results import ResultsView
ResultsView.register(app)
