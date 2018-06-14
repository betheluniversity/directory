from flask import Flask
from flask_caching import Cache

import datetime

app = Flask(__name__)
app.config.from_object('config')
cache = Cache(app, config={'CACHE_TYPE': 'simple'})
# TODO: Production cache

# Shows the year for the template
app.jinja_env.globals.update(now=datetime.datetime.now())

from app.db import db_functions as db

from app.views.home import HomeView

HomeView.register(app, route_base='/')


@app.route('/logout', methods=['GET'])
def logout(self):
    pass
